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



# class ExpencesView(LoginRequiredMixin,date_day_to.ToSalary, generic.TemplateView):
#     template_name = "expences/main.html"
#     login_url = reverse_lazy('login')
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         x = date_day_to.ToSalary()
#         context["days_to_salary"] = x.days_to_salary
#         context["money_to_salary"] = self.request.user.user_per_day.value * x.days_to_salary
#         context["reserv"] = self.request.user.user_reserv.value
#         not_paid= models.IncomeAndExpediture.objects.filter(Q(user = self.request.user) & Q(status=False))
#         sum_of_not_paid = 0 
#         for val in not_paid:
#             sum_of_not_paid += val.value
#         context["not_paid"] = sum_of_not_paid
#         context["ost"] = (self.request.user.user_per_day.value * x.days_to_salary) + self.request.user.user_reserv.value + sum_of_not_paid
#         additional = models.AdditionalIncome.objects.filter(Q(user = self.request.user) & Q(date__year=date_day_to.date.year,
#     date__month=date_day_to.date.month))
#         sum_of_additional = 0
#         for add in additional:
#             sum_of_additional += add.value
#         context["additional"] = sum_of_additional
#         # income = models.Salary.objects.filter(Q(user = self.request.user)& Q(status=True))
#         # print(income)
#         # out = models.IncomeAndExpediture.objects.filter(Q(user = self.request.user) & Q(status = False))
#         # print(out)
#         # sum_of_income = 0 
#         # for val in income:
#         #     sum_of_income += val.value
#         # sum_of_out = 0
#         # for val in out:
#         #     sum_of_out += val.value
#         # context['reserv'] = sum_of_income - sum_of_out - self.request.user.user_per_day.value * x.days_to_salary
#         # print (sum_of_income)
#         return context
    
def expences_view(request):
    context = {}
    x = date_day_to.ToSalary()
    context["days_to_salary"] = x.days_to_salary
    context["money_to_salary"] = request.user.user_per_day.value * x.days_to_salary
    context["reserv"] = request.user.user_reserv.value
    not_paid= models.IncomeAndExpediture.objects.filter(Q(user = request.user) & Q(status=False))
    sum_of_not_paid = 0 
    for val in not_paid:
        sum_of_not_paid += val.value
    context["not_paid"] = sum_of_not_paid
    ost = (request.user.user_per_day.value * x.days_to_salary) + request.user.user_reserv.value + sum_of_not_paid
    context["ost"] = ost
    additional = models.AdditionalIncome.objects.filter(Q(user = request.user) & Q(date__year=date_day_to.date.year,
    date__month=date_day_to.date.month))
    sum_of_additional = 0
    for add in additional:
        sum_of_additional += add.value
    context["additional"] = sum_of_additional

    if request.method == 'POST':
        balance = request.POST.get('balance')
        context['balance'] = balance
        differenc = int(balance) - int(ost)
        context['difference'] = differenc
        resrv  = request.user.user_reserv.value + differenc
        context['real_reserv'] = resrv


    return render(
        request=request,
        template_name="expences/main.html",
        context=context
    )

# расходы


class CreateExpences(LoginRequiredMixin,generic.CreateView):
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
    
class UpdateExpences(LoginRequiredMixin,generic.UpdateView):
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

class DeleteExpences(LoginRequiredMixin,generic.DeleteView):
    model = models.IncomeAndExpediture
    template_name = "expences/delete_expences.html"
    success_url = reverse_lazy('expences:list')
    login_url = reverse_lazy('expences:main')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Удаление'
        context["alert_message"] = 'Вы точно хотите удалить данную сторку расходов???'
        return context


class ListExpences(LoginRequiredMixin,generic.ListView):
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
        object_list_2 = models.IncomeAndExpediture.objects.filter(Q(user=user) & Q(status = False))
        total = 0
        for obj in object_list_2:
            total += obj.value
        context['total'] = total
        return context
    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     return self.form_valid(form)
    

class DetailExpences(LoginRequiredMixin,generic.DetailView):
    model = models.IncomeAndExpediture
    template_name = "expences/detail_expences.html"
    login_url = reverse_lazy('login')




#  зарплата/аванс


class CreateIncome(LoginRequiredMixin,generic.CreateView):
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
    
class UpdateIncome(LoginRequiredMixin,generic.UpdateView):
    model = models.Salary
    form_class = forms.SalaryForm
    template_name = "expences/edit_expences.html"
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('expences:list-s')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить'
        return context
    

class DeleteIncome(LoginRequiredMixin,generic.DeleteView):
    model = models.Salary
    template_name = "expences/delete_expences.html"
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('expences:list-s')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Удаление'
        context["alert_message"] = 'Вы точно хотите удалить данную запись о зарплате(авансе)???'
        return context


class ListIncome(LoginRequiredMixin,generic.ListView):
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
    
    

class DetailIncome(LoginRequiredMixin,generic.DetailView):
    model = models.Salary
    template_name = "expences/detail_expences.html"
    login_url = reverse_lazy('login')



# PerDay/дневной расход 

class CreatePerDay (LoginRequiredMixin,generic.CreateView):
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
    
class UpdatePerDay(LoginRequiredMixin,generic.UpdateView):
    model = models.PerDay
    form_class = forms.PerDayForm
    template_name = "expences/edit_expences.html"
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('expences:main')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить'
        return context

    
class DetailPerDay(LoginRequiredMixin,generic.DetailView):
    model = models.PerDay
    login_url = reverse_lazy('login')
    template_name = "expences/detil_expences.html"
    def get_queryset(self):
        user = self.request.user
        object_list = models.PerDay.objects.filter(user=user)
        return object_list


# резерв

class UpdateReserv(LoginRequiredMixin,generic.UpdateView):
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

class CreateAdditional(LoginRequiredMixin,generic.CreateView):
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

class UpdateAdditional(LoginRequiredMixin,generic.UpdateView):
    model = models.AdditionalIncome
    template_name = "expences/edit_expences.html"
    form_class = forms.AdditionalIncomeForm
    success_url = reverse_lazy('expences:main')
    login_url = reverse_lazy('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить дополнительный доход'
        return context

class DeleteAdditional(LoginRequiredMixin,generic.DeleteView):
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
        object_list = models.AdditionalIncome.objects.filter(user = self.request.user)
        return object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = models.AdditionalIncome.objects.filter(user = self.request.user)
        total = 0
        for object in object_list:
            total += object.value
        context["total"] = total
        return context




