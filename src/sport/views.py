from django.shortcuts import render, redirect
from . import models, forms
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime


class HomepageView(LoginRequiredMixin,generic.TemplateView):
    login_url = reverse_lazy('login')
    template_name = "sport/sport_main.html"

class SubscriptionView(LoginRequiredMixin,generic.TemplateView):
    template_name = "sport/subscription.html"
    login_url = reverse_lazy('login')



class SubscriptionCreateView(LoginRequiredMixin,generic.CreateView):
    model = models.SubscriptionModel
    form_class = forms.SubscriptionForm    
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('sport:subscription')
    template_name = "sport/edit_subscription.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Добавить абонемент'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SubscriptionUpdateView(UserPassesTestMixin, LoginRequiredMixin, generic.UpdateView):
    model = models.SubscriptionModel
    form_class = forms.SubscriptionForm
    template_name = "sport/edit_subscription.html"
    success_url = reverse_lazy('sport:subscription')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Внести изменения'
        return context


    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False


class SubscriptionDeleteView(UserPassesTestMixin, LoginRequiredMixin, generic.DeleteView):
    model = models.SubscriptionModel
    template_name = "sport/delete_subscription.html"
    success_url = reverse_lazy('sport:subscription')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Удаление абонемента'
        context["alert_message"] = 'Вы точно хотите удалить данный абонемент???'
        return context

    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False

class SubscriptionDetailView(UserPassesTestMixin, LoginRequiredMixin, generic.DetailView):
    model = models.SubscriptionModel
    template_name = "sport/detail_subscription.html"
    login_url = reverse_lazy('login')

    def test_func(self):
        for_test = self.get_object()
        if self.request.user == for_test.user:
            return True
        else:
            return False


class SubscriptionListView(LoginRequiredMixin, generic.ListView):
    model = models.SubscriptionModel
    template_name = "sport/list_subscription.html"
    login_url = reverse_lazy('login')

    def get_queryset(self):
        object_list = models.SubscriptionModel.objects.filter(
            user=self.request.user)
        return object_list

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     object_list = models.Expediture.objects.filter(user=user)
    #     total_to_pay = 0
    #     for obj in object_list:
    #         total_to_pay += obj.value
    #     context["total_to_pay"] = total_to_pay
    #     object_list_2 = models.Expediture.objects.filter(
    #         Q(user=user) & Q(status=False))
    #     total = 0
    #     for obj in object_list_2:
    #         total += obj.value
    #     daily_consumption = user.user_daily_cons.per_month
    #     context['daily_consumption'] = daily_consumption
    #     context['total_exp'] = total
    #     context['total'] = total + daily_consumption
    #     return context




# ##################################################################################



class SubscriptionVisitCreateView(LoginRequiredMixin,generic.CreateView):
    model = models.SubscriptionVisit
    form_class = forms.SubscriptionVisitsForm
    login_url = reverse_lazy('login')
    # success_url = reverse_lazy(':list')
    template_name = "sport/add_train.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation"] = 'Создать'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)