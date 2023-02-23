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
    template_name = "sport/edit_subscription.html"



class SubscriptionVisitCreateView(LoginRequiredMixin,generic.CreateView):
    model = models.SubscriptionVisit
    form_class = forms.SubscriptionVisitsForm
    login_url = reverse_lazy('login')
    template_name = "sport/add_train.html"
