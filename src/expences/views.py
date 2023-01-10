from django.shortcuts import render
from . import models, forms
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from . import date_day_to
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required


@login_required
def expences_view(request):
    context = {}
    x = date_day_to.ToSalary()
    # дни до зарплаты
    context["days_to_salary"] = x.days_to_salary
    # сумма на карте до конца месяца на ежедневные расходы
    context["money_to_salary"] = request.user.user_per_day.value * x.days_to_salary
    # сумма резерва на карте
    context["reserv"] = request.user.user_reserv.value
    # не оплаченные услуги
    not_paid = models.IncomeAndExpediture.objects.filter(Q(user=request.user) & Q(status=False))
    sum_of_not_paid = 0
    for val in not_paid:
        sum_of_not_paid += val.value
    context["not_paid"] = sum_of_not_paid
    # ожидаемый остаток на карте(исходя из данных)
    ost = (request.user.user_per_day.value * x.days_to_salary) + request.user.user_reserv.value + sum_of_not_paid
    context["ost"] = ost
    # дополнителнительные доходы за текущий месяц
    additional = models.AdditionalIncome.objects.filter(Q(user=request.user) & Q(date__year=date_day_to.date.year,
                                                                                 date__month=date_day_to.date.month))
    sum_of_additional = 0
    for add in additional:
        sum_of_additional += add.value
    context["additional"] = sum_of_additional

    #временно фильтровать по статусу. далее автоматически
    salary_for_mounth = models.Salary.objects.filter(Q(user = request.user) & Q(status = True))
    sum_of_salary = 0
    for salary in salary_for_mounth:
        sum_of_salary += salary.value
    context["salary_for_mounth"] = sum_of_salary



    # автоматическое обновление статуса рсходов после получения ЗП(когда до ЗП 0(ноль) дней)
    #но в этот день, получается нельзя будет отметить оплату, т.к при обновлении страницы в этот день будет сбрасывать статус
    if x.days_to_salary == 0:
        all_expediture = models.IncomeAndExpediture.objects.filter(user = request.user)
        print(all_expediture)
        for expediture in all_expediture:
            expediture.status = False
            expediture.save()

    #  основной доход за расчетный месяц
    #...................................


    # форма для уточнения резерва исходя из реального(данные которые введут) остатка на карте (!нужно дополнительно ввести в расчет аванс)
    if request.method == 'POST':
        balance = request.POST.get('balance')
        context['balance'] = balance
        difference = int(balance) - int(ost)
        context['difference'] = difference
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
        user = self.request.user
        object_list = models.IncomeAndExpediture.objects.filter(user=user)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        object_list = models.IncomeAndExpediture.objects.filter(user=user)
        total_to_pay = 0
        for obj in object_list:
            total_to_pay += obj.value
        context["total_to_pay"] = total_to_pay
        object_list_2 = models.IncomeAndExpediture.objects.filter(Q(user=user) & Q(status=False))
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
        object_list = models.AdditionalIncome.objects.filter(user=self.request.user)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = models.AdditionalIncome.objects.filter(user=self.request.user)
        total = 0
        for object in object_list:
            total += object.value
        context["total"] = total
        return context
