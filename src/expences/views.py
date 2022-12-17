from django.shortcuts import render
from . import models, forms
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from . import mixins
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class ExpencesView(mixins.ToSalary, generic.TemplateView):
    template_name = "expences/main.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        x = mixins.ToSalary()
        context["days_to_salary"] = x.days_to_salary
        context["money_to_salary"] = self.request.user.user_per_day.value * x.days_to_salary
        return context
    

# расходы


class CreateExpences(generic.CreateView):
    model = models.IncomeAndExpediture
    form_class = forms.ExpencesForms
    template_name = "expences/edit_expences.html"
    success_url = reverse_lazy('expences:list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Создать'
        return context
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
    
class UpdateExpences(generic.UpdateView):
    model = models.IncomeAndExpediture
    form_class = forms.ExpencesForms
    template_name = "expences/edit_expences.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить'
        return context
    

class DeleteExpences(generic.DeleteView):
    model = models.IncomeAndExpediture
    template_name = "expences/delete_expences.html"
    success_url = reverse_lazy('expences:list')


class ListExpences(generic.ListView):
    model = models.IncomeAndExpediture
    template_name = "expences/list_expences.html"
    def get_queryset(self):
        user = self.request.user
        object_list = models.IncomeAndExpediture.objects.filter(user=user)
        return object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        object_list = models.IncomeAndExpediture.objects.filter(user=user)
        total = 0
        for obj in object_list:
            total += obj.value
        context["total"] = total
        return context
    
    

class DetailExpences(generic.DetailView):
    model = models.IncomeAndExpediture
    template_name = "expences/detail_expences.html"




#  доход


class CreateIncome(generic.CreateView):
    model = models.Salary
    form_class = forms.SalaryForms
    template_name = "expences/edit_expences.html"
    success_url = reverse_lazy('expences:list-s')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Создать'
        return context
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
    
class UpdateIncome(generic.UpdateView):
    model = models.Salary
    form_class = forms.SalaryForms
    template_name = "expences/edit_expences.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить'
        return context
    

class DeleteIncome(generic.DeleteView):
    model = models.Salary
    template_name = "expences/delete_expences.html"
    success_url = reverse_lazy('expences:list-s')


class ListIncome(generic.ListView):
    model = models.Salary
    template_name = "expences/list_expences-s.html"
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
    
    

class DetailIncome(generic.DetailView):
    model = models.Salary
    template_name = "expences/detail_expences.html"



# PerDay/дневной расход 

class CreatePerDay (generic.CreateView):
    model = models.PerDay
    form_class = forms.PerDayForms
    template_name = "expences/edit_expences.html"
    success_url = reverse_lazy('expences:main')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Создать'
        return context
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
    
class UpdatePerDay(generic.UpdateView):
    model = models.PerDay
    form_class = forms.PerDayForms
    template_name = "expences/edit_expences.html"
    success_url = reverse_lazy('expences:main')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Изменить'
        return context

    
class DetailPerDay(generic.DetailView):
    model = models.PerDay
    template_name = "expences/detil_expences.html"
    def get_queryset(self):
        user = self.request.user
        object_list = models.PerDay.objects.filter(user=user)
        return object_list