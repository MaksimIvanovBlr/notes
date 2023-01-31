from django.shortcuts import render, redirect
from . import models, forms
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import date_day_to
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


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
def expences_view(request):
    try:
        context = {}
        x = date_day_to.ToSalary()
        # дни до зарплаты
        context["days_to_salary"] = x.days_to_salary
        # сумма на карте до конца месяца на ежедневные расходы
        context["money_to_salary"] = request.user.user_per_day.value * \
            x.days_to_salary
        # сумма резерва на карте
        reserv, created = models.Reserv.objects.get_or_create(
            user=request.user,
            defaults={'value': 0}
        )
        if created:
            context['created'] = 'Для расчета необходимо указать ЗП за текущий месяц,обязательные расходы, а потом сделать перерасчет(пересчитать резерв). Данные пункты будут обозначанны "!" '
            context['attention'] = '!'
        context["reserv"] = reserv.value
        # не оплаченные услуги
        not_paid = models.IncomeAndExpediture.objects.filter(
            Q(user=request.user) & Q(status=False))
        sum_of_not_paid = 0
        for val in not_paid:
            sum_of_not_paid += val.value
        context["not_paid"] = sum_of_not_paid

        # дополнителнительные доходы за текущий месяц
        additional = models.AdditionalIncome.objects.filter(Q(user=request.user) & Q(date__year=date_day_to.date.year,
                                                                                     date__month=date_day_to.date.month))
        sum_of_additional = 0
        for add in additional:
            sum_of_additional += add.value
        context["additional"] = sum_of_additional

        # сумма дополнительных доходов, которые еще не использованны, но все еще на карте
        not_used_additional = models.AdditionalIncome.objects.filter(Q(user=request.user) & Q(status=True))
        sum_of_not_used_additional = 0
        for not_used in not_used_additional:
            sum_of_not_used_additional += not_used.value
        context['not_used_additional'] = sum_of_not_used_additional

        # ожидаемый остаток на карте(исходя из данных)
        last_transfer = models.Salary.objects.all().order_by('-id')[:1]
        main_ost = (request.user.user_per_day.value * x.days_to_salary) + \
                request.user.user_reserv.value + sum_of_not_paid + sum_of_not_used_additional
        if last_transfer[0].name == 'аванс':
            ost = main_ost + last_transfer[0].value

        else:
            ost = main_ost

        context["ost"] = ost

        # буферная сумма- разница между реальным балансом и прогнозируемым
        real_user_balance = request.user.user_per_day
        buffer_money = int(real_user_balance.balance) - int(ost)
        context['real_balance'] = real_user_balance.balance
        context['buffer_money'] = buffer_money

        # временно фильтровать по статусу. далее автоматически
        salary_for_mounth = models.Salary.objects.filter(
            Q(user=request.user) & Q(status=True))
        sum_of_salary = 0
        for salary in salary_for_mounth:
            sum_of_salary += salary.value
        context["salary_for_mounth"] = sum_of_salary

        # автоматическое обновление статуса расходов после получения ЗП(когда до ЗП 0(ноль) дней) но в этот день,
        # получается нельзя будет отметить оплату, т.к при обновлении страницы в этот день будет сбрасывать статус
        if x.days_to_salary == 0:
            #
            all_expediture = models.IncomeAndExpediture.objects.filter(
                user=request.user)
            for expediture in all_expediture:
                expediture.status = False
                expediture.save()
            user_salary = models.Salary.objects.filter(
                Q(user=request.user) & Q(name='зарплата') & Q(status=True))
            if user_salary:
                request.user.user_reserv.value = sum_of_salary - sum_of_not_paid - (
                    request.user.user_per_day.value * 31)
                request.user.user_reserv.save()

        # форма для уточнения резерва исходя из реального(данные которые введут) остатка на карте
        if request.method == 'POST':
            balance = request.POST.get('balance')
            difference = int(balance) - int(ost)
            context['difference'] = difference
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
    if request.method == "POST":

        salary_for_mounth = models.Salary.objects.filter(
            Q(user=request.user) & Q(status=True))
        sum_of_salary = 0
        for salary in salary_for_mounth:
            sum_of_salary += salary.value

        x = date_day_to.ToSalary()
        if x.days_to_salary != 0:
            days_to_next_salary = x.days_to_salary
        else:
            days_to_next_salary = 31

        all_expediture = models.IncomeAndExpediture.objects.filter(
            user=request.user)
        for expediture in all_expediture:
            expediture.status = False
            expediture.save()

        #  сумма неоплаченных ежемесячных платежей
        not_paid = models.IncomeAndExpediture.objects.filter(
            Q(user=request.user) & Q(status=False))
        sum_of_not_paid = 0
        for val in not_paid:
            sum_of_not_paid += val.value
        context["not_paid"] = sum_of_not_paid

        request.user.user_reserv.value = sum_of_salary - sum_of_not_paid - (
            request.user.user_per_day.value * days_to_next_salary)
        request.user.user_reserv.save()

    return render(
        request=request,
        context=context,
        template_name='expences/recalculation.html'

    )


# расходы

class CreateExpences(LoginRequiredMixin, generic.CreateView):
    model = models.IncomeAndExpediture
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


class UpdateExpences(LoginRequiredMixin, generic.UpdateView):
    model = models.IncomeAndExpediture
    form_class = forms.ExpencesForm
    template_name = "expences/edit_expences.html"
    success_url = reverse_lazy('expences:list')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить'
        return context

    def get_success_url(self):
        # тут нужно добавить логику расчета резерва
        return super().get_success_url()


class DeleteExpences(LoginRequiredMixin, generic.DeleteView):
    model = models.IncomeAndExpediture
    template_name = "expences/delete_expences.html"
    success_url = reverse_lazy('expences:list')
    login_url = reverse_lazy('expences:main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Удаление'
        context["alert_message"] = 'Вы точно хотите удалить данную сторку расходов???'
        return context


class ListExpences(LoginRequiredMixin, generic.ListView):
    model = models.IncomeAndExpediture
    template_name = "expences/list_expences.html"
    login_url = reverse_lazy('login')

    # from_class = forms.ExpencesForms
    def get_queryset(self):
        object_list = models.IncomeAndExpediture.objects.filter(
            user=self.request.user)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        object_list = models.IncomeAndExpediture.objects.filter(user=user)
        total_to_pay = 0
        for obj in object_list:
            total_to_pay += obj.value
        context["total_to_pay"] = total_to_pay
        object_list_2 = models.IncomeAndExpediture.objects.filter(
            Q(user=user) & Q(status=False))
        total = 0
        for obj in object_list_2:
            total += obj.value
        context['total'] = total
        return context
    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     return self.form_valid(form)


class DetailExpences(LoginRequiredMixin, generic.DetailView):
    model = models.IncomeAndExpediture
    template_name = "expences/detail_expences.html"
    login_url = reverse_lazy('login')


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


class UpdateIncome(LoginRequiredMixin, generic.UpdateView):
    model = models.Salary
    form_class = forms.SalaryForm
    template_name = "expences/edit_expences.html"
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('expences:list-s')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить'
        return context


class DeleteIncome(LoginRequiredMixin, generic.DeleteView):
    model = models.Salary
    template_name = "expences/delete_expences.html"
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('expences:list-s')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Удаление'
        context["alert_message"] = 'Вы точно хотите удалить данную запись о зарплате(авансе)???'
        return context


class ListIncome(LoginRequiredMixin, generic.ListView):
    model = models.Salary
    template_name = "expences/list_expences-s.html"
    login_url = reverse_lazy('login')

    def get_queryset(self):
        user = self.request.user
        object_list = models.Salary.objects.filter(user=user)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        object_list = models.Salary.objects.filter(user=user)
        total = 0
        for obj in object_list:
            total += obj.value
        context["total"] = total
        return context


class DetailIncome(LoginRequiredMixin, generic.DetailView):
    model = models.Salary
    template_name = "expences/detail_expences.html"
    login_url = reverse_lazy('login')


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


class UpdatePerDay(LoginRequiredMixin, generic.UpdateView):
    model = models.PerDay
    form_class = forms.PerDayForm
    template_name = "expences/edit_expences.html"
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('expences:main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить'
        return context


class DetailPerDay(LoginRequiredMixin, generic.DetailView):
    model = models.PerDay
    login_url = reverse_lazy('login')
    template_name = "expences/detil_expences.html"

    def get_queryset(self):
        user = self.request.user
        object_list = models.PerDay.objects.filter(user=user)
        return object_list


# резерв

class UpdateReserv(LoginRequiredMixin, generic.UpdateView):
    model = models.Reserv
    login_url = reverse_lazy('login')
    template_name = "expences/edit_reserv.html"
    success_url = reverse_lazy('expences:main')
    form_class = forms.ReservForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить резерв'
        return context


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


class UpdateAdditional(LoginRequiredMixin, generic.UpdateView):
    model = models.AdditionalIncome
    template_name = "expences/edit_expences.html"
    form_class = forms.AdditionalIncomeForm
    success_url = reverse_lazy('expences:main')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить дополнительный доход'
        return context


class DeleteAdditional(LoginRequiredMixin, generic.DeleteView):
    model = models.AdditionalIncome
    template_name = "expences/delete_expences.html"
    success_url = reverse_lazy('expences:main')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Удаление'
        context["alert_message"] = 'Вы точно хотите удалить данную запись о допонительном доходе???'
        return context


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
