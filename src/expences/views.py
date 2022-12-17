from django.shortcuts import render
from . import models, forms
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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
    

class DetailExpences(generic.DetailView):
    model = models.IncomeAndExpediture
    template_name = "expences/detil_expences.html"

class ExpencesView(generic.TemplateView):

    template_name = "expences/main.html"
