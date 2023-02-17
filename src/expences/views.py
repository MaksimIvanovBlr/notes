from django.shortcuts import render, redirect
from . import models, forms
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime

def day_to(request):
    now_date = datetime.now()
    # now_date = datetime(2021.10.15) => for test
    user_date = request.user.user_per_day.day.day
    some_date2 = datetime(now_date.year, now_date.month, user_date)
    if now_date.month == 12:
        some_date = datetime(now_date.year + 1, 1, user_date)
    else:
        some_date = datetime(now_date.year, now_date.month + 1, user_date)
    
    if now_date.day < some_date.day:
        day_to_salary1 = some_date2 - now_date
    else:
        day_to_salary1 = some_date - now_date
    day_to_salary1 = day_to_salary1.days
    return day_to_salary1

class AddBaseInfoView(LoginRequiredMixin, generic.CreateView):
    model = models.PerDay
    form_class = forms.PerDayForm
    success_url = reverse_lazy('expences:main')
    login_url = reverse_lazy('login')
    template_name = 'expences/add_base_info.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



@login_required(login_url='login')
def daily_consumption(request):
    context = {}
    
    day_to_salary1 = day_to(request=request)

    buffer_money = request.user.user_daily_cons.per_month - (request.user.user_per_day.value * day_to_salary1) 
    daily_consumption = request.user.user_daily_cons
    daily_consumption.buffer_money += buffer_money
    daily_consumption.per_month = request.user.user_per_day.value * day_to_salary1
    daily_consumption.save()



    context['per_month'] = request.user.user_daily_cons.per_month
    context['buffer_money'] = request.user.user_daily_cons.buffer_money
    context['days'] = request.user.user_daily_cons.per_month /  request.user.user_per_day.value

    if request.method == "POST":
        spend_money = int(request.POST.get('spend_money'))
        context['spend_money'] = spend_money
        reserv = request.user.user_reserv
        if spend_money > daily_consumption.buffer_money:
            spend_money -= daily_consumption.buffer_money
            reserv.value -= spend_money
            daily_consumption.buffer_money = 0
            daily_consumption.save()
            reserv.save()


            context['alarm'] = 'Вы привысили лимит! Разница будет списана с "резерва".'
            context['reserv_value'] = reserv.value
            context['sum_that_gt'] = abs(daily_consumption.buffer_money - spend_money)

        else:
            daily_consumption.buffer_money -= spend_money
            daily_consumption.save()
            context['spend_money_lt_buffer'] = daily_consumption.buffer_money 

    return render(
            request=request,
            template_name="expences/daily_consumption.html",
            context=context
        )




@login_required(login_url='login')
def expences_view(request):
    try:
        context = {}
        #расчет даты
        day_to_salary1 = day_to(request=request)
        # дни до зарплаты
        context["days_to_salary"] = day_to_salary1
        # сумма на карте до конца месяца на ежедневные расходы

        daily, created = models.DailyConsumption.objects.get_or_create(
            user=request.user,
            defaults={'per_month': day_to_salary1 * request.user.user_per_day.value,
                    'buffer_money': 0            
            }
        )
        context["money_to_salary"] = request.user.user_daily_cons.per_month

        # сумма резерва на карте
        reserv, created = models.Reserv.objects.get_or_create(
            user=request.user,
            defaults={'value': 0}
        )
        if created:
            context[
                'created'] = 'Для расчета необходимо указать ЗП за текущий месяц,обязательные расходы, а потом сделать перерасчет(пересчитать резерв). Данные пункты будут обозначанны "!" '
            context['attention'] = '!'
        context["reserv"] = reserv.value
        # не оплаченные услуги
        not_paid = models.Expediture.objects.filter(
            Q(user=request.user) & Q(status=False))
        sum_of_not_paid = 0
        for val in not_paid:
            sum_of_not_paid += val.value
        context["not_paid"] = sum_of_not_paid

        # сумма дополнительных доходов, которые еще не использованны и все еще на карте
        not_used_additional = models.AdditionalIncome.objects.filter(
            Q(user=request.user) & Q(status=False))
        sum_of_not_used_additional = 0
        for not_used in not_used_additional:
            sum_of_not_used_additional += not_used.value
        context['not_used_additional'] = sum_of_not_used_additional

        # ожидаемый остаток на карте(исходя из данных)
        last_transfer = models.Salary.objects.filter(user = request.user).order_by('-id')[:1]

        ost = request.user.user_daily_cons.per_month + request.user.user_daily_cons.buffer_money + \
            request.user.user_reserv.value + sum_of_not_paid + sum_of_not_used_additional

        if last_transfer:
            if last_transfer[0].name == 'аванс':
                ost += last_transfer[0].value
        context["ost"] = ost

        # буферная сумма и реальный(указанный пользователем баланс карты)
        if request.user.user_per_day.balance:
            context['real_balance'] = request.user.user_per_day.balance
        else:
            context['real_balance'] = 0

        if request.user.user_daily_cons.buffer_money:
            context['buffer_money'] = request.user.user_daily_cons.buffer_money
        else:
            context['buffer_money'] = 0
        

        # временно фильтровать по статусу. далее автоматически
        salary_for_mounth = models.Salary.objects.filter(
            Q(user=request.user) & Q(status=True))
        sum_of_salary = 0
        for salary in salary_for_mounth:
            sum_of_salary += salary.value
        context["salary_for_mounth"] = sum_of_salary

    

        # форма для уточнения резерва исходя из реального(данные которые введут) остатка на карте
        if request.method == 'POST':
            balance = request.POST.get('balance')
            difference = int(balance) - int(ost)
            context['difference'] = difference
            real_user_balance = request.user.user_per_day
            real_user_balance.balance = balance
            real_user_balance.save()
            resrv = request.user.user_reserv.value + difference
            context['real_reserv'] = resrv
            user_res = request.user.user_reserv
            user_res.value = resrv
            user_res.save()

        return render(
            request=request,
            template_name="expences/main.html",
            context=context
        )
    except User.user_per_day.RelatedObjectDoesNotExist:
        return redirect('expences:create-base-info')


@login_required(login_url='login')
def recalculation(request):
    context = {}

    day_to_salary1 = day_to(request=request)

    if request.method == "POST":

        salary_for_mounth = models.Salary.objects.filter(
            Q(user=request.user) & Q(status=True))
        sum_of_salary = 0
        for salary in salary_for_mounth:
            sum_of_salary += salary.value

        all_expediture = models.Expediture.objects.filter(
            user=request.user)
        for expediture in all_expediture:
            expediture.status = False
            expediture.save()

        #  сумма неоплаченных ежемесячных платежей
        not_paid = models.Expediture.objects.filter(
            Q(user=request.user) & Q(status=False))
        sum_of_not_paid = 0
        for val in not_paid:
            sum_of_not_paid += val.value
        context["not_paid"] = sum_of_not_paid
        
        if day_to_salary1 == 0:
            user_day_to_salary1 = 31
        else:
            user_day_to_salary1 = day_to_salary1 
        
        daily_consumption = request.user.user_daily_cons
        daily_consumption.per_month = request.user.user_per_day.value * day_to_salary1
        daily_consumption.save()

        request.user.user_reserv.value = sum_of_salary - sum_of_not_paid - (
            request.user.user_per_day.value * user_day_to_salary1)
        request.user.user_reserv.value_of_days_exp = request.user.user_per_day.value * user_day_to_salary1
        request.user.user_reserv.save()

    return render(
        request=request,
        context=context,
        template_name='expences/recalculation.html'

    )


# расходы

class CreateExpences(LoginRequiredMixin, generic.CreateView):
    model = models.Expediture
    form_class = forms.ExpencesForm
    template_name = "expences/edit_expences.html"
    success_url = reverse_lazy('expences:list')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Создать'
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)


class UpdateExpences(UserPassesTestMixin, LoginRequiredMixin, generic.UpdateView):
    model = models.Expediture
    form_class = forms.ExpencesForm
    template_name = "expences/edit_expences.html"
    success_url = reverse_lazy('expences:list')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить'
        return context


    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False


class DeleteExpences(UserPassesTestMixin, LoginRequiredMixin, generic.DeleteView):
    model = models.Expediture
    template_name = "expences/delete_expences.html"
    success_url = reverse_lazy('expences:list')
    login_url = reverse_lazy('expences:main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Удаление'
        context["alert_message"] = 'Вы точно хотите удалить данную сторку расходов???'
        return context

    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False


class ListExpences(LoginRequiredMixin, generic.ListView):
    model = models.Expediture
    template_name = "expences/list_expences.html"
    login_url = reverse_lazy('login')

    def get_queryset(self):
        object_list = models.Expediture.objects.filter(
            user=self.request.user)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        object_list = models.Expediture.objects.filter(user=user)
        total_to_pay = 0
        for obj in object_list:
            total_to_pay += obj.value
        context["total_to_pay"] = total_to_pay
        object_list_2 = models.Expediture.objects.filter(
            Q(user=user) & Q(status=False))
        total = 0
        for obj in object_list_2:
            total += obj.value
        daily_consumption = user.user_daily_cons.per_month
        context['daily_consumption'] = daily_consumption
        context['total_exp'] = total
        context['total'] = total + daily_consumption
        return context


class DetailExpences(UserPassesTestMixin, LoginRequiredMixin, generic.DetailView):
    model = models.Expediture
    template_name = "expences/detail_expences.html"
    login_url = reverse_lazy('login')

    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False

#  зарплата/аванс


class CreateIncome(LoginRequiredMixin, generic.CreateView):
    model = models.Salary
    form_class = forms.SalaryForm
    template_name = "expences/edit_expences.html"
    success_url = reverse_lazy('expences:list-s')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Создать'
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)


class UpdateIncome(UserPassesTestMixin, LoginRequiredMixin, generic.UpdateView):
    model = models.Salary
    form_class = forms.SalaryForm
    template_name = "expences/edit_expences.html"
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('expences:list-s')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить'
        return context

    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False


class DeleteIncome(UserPassesTestMixin, LoginRequiredMixin, generic.DeleteView):
    model = models.Salary
    template_name = "expences/delete_expences.html"
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('expences:list-s')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Удаление'
        context["alert_message"] = 'Вы точно хотите удалить данную запись о зарплате(авансе)???'
        return context

    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False


class ListIncome(LoginRequiredMixin, generic.ListView):
    model = models.Salary
    template_name = "expences/list_expences-s.html"
    login_url = reverse_lazy('login')

    def get_queryset(self):
        object_list = models.Salary.objects.filter(user=self.request.user)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = models.Salary.objects.filter(user=self.request.user)
        total = 0
        for obj in object_list:
            total += obj.value
        context["total"] = total
        return context


class DetailIncome(UserPassesTestMixin, LoginRequiredMixin, generic.DetailView):
    model = models.Salary
    template_name = "expences/detail_expences.html"
    login_url = reverse_lazy('login')

    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False


# PerDay/дневной расход

class CreatePerDay(LoginRequiredMixin, generic.CreateView):
    model = models.PerDay
    form_class = forms.PerDayForm
    template_name = "expences/edit_expences.html"
    success_url = reverse_lazy('expences:main')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Создать'
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)


class UpdatePerDay(UserPassesTestMixin, LoginRequiredMixin, generic.UpdateView):
    model = models.PerDay
    form_class = forms.PerDayForm
    template_name = "expences/edit_expences.html"
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('expences:main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить'
        return context

    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False
    
    def get_success_url(self):
        day = day_to(request=self.request)
        if day == 0:
            day_to_salary1 = 31
        else:
            day_to_salary1 = day
        
        daily_consumption = self.request.user.user_daily_cons
        daily_consumption.per_month = self.request.user.user_per_day.value * day_to_salary1
        daily_consumption.save()

        return super().get_success_url()


class DetailPerDay(UserPassesTestMixin, LoginRequiredMixin, generic.DetailView):
    model = models.PerDay
    login_url = reverse_lazy('login')
    template_name = "expences/detil_expences.html"

    def get_queryset(self):
        user = self.request.user
        object_list = models.PerDay.objects.filter(user=user)
        return object_list

    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False

# резерв


class UpdateReserv(UserPassesTestMixin, LoginRequiredMixin, generic.UpdateView):
    model = models.Reserv
    login_url = reverse_lazy('login')
    template_name = "expences/edit_reserv.html"
    success_url = reverse_lazy('expences:main')
    form_class = forms.ReservForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить резерв'
        return context

    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False


# дополнительных доход

class CreateAdditional(LoginRequiredMixin, generic.CreateView):
    model = models.AdditionalIncome
    template_name = "expences/edit_expences.html"
    form_class = forms.AdditionalIncomeForm
    success_url = reverse_lazy('expences:main')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Добавить дополнительный доход'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateAdditional(UserPassesTestMixin, LoginRequiredMixin, generic.UpdateView):
    model = models.AdditionalIncome
    template_name = "expences/edit_expences.html"
    form_class = forms.AdditionalIncomeForm
    success_url = reverse_lazy('expences:main')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить дополнительный доход'
        return context

    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False


class DeleteAdditional(UserPassesTestMixin, LoginRequiredMixin, generic.DeleteView):
    model = models.AdditionalIncome
    template_name = "expences/delete_expences.html"
    success_url = reverse_lazy('expences:main')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Удаление'
        context["alert_message"] = 'Вы точно хотите удалить данную запись о допонительном доходе???'
        return context

    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False


class ListAdditional(generic.ListView):
    model = models.AdditionalIncome
    template_name = "expences/list_expences-a.html"

    def get_queryset(self):
        object_list = models.AdditionalIncome.objects.filter(
            user=self.request.user)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = models.AdditionalIncome.objects.filter(
            user=self.request.user)
        total = 0
        for object in object_list:
            total += object.value
        context["total"] = total
        return context
