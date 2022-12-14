from django.shortcuts import render
from . import models, forms
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class Budgeting(generic.TemplateView):
    template_name = 'budgeting/main.html'

class AddExpenses(generic.CreateView):
    model = models.Expenses
    form_class = forms.ExpensesForm
    template_name = 'budgeting/edit_expenses.html'
    success_url = reverse_lazy('homepage:home')

class UpdateExpenses(generic.UpdateView):
    model = models.Expenses
    form_class = forms.ExpensesForm
    template_name = 'budgeting/edit_expenses.html'
    success_url = reverse_lazy('homepage:home')

class DetailExpenses(generic.DetailView):
    model = models.Expenses
    template_name = 'budgeting/detail_expenses.html'

