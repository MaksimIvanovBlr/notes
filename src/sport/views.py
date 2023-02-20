from django.shortcuts import render, redirect
from . import models, forms
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime


class HomepageView(generic.TemplateView):
    template_name = "sport/sport_main.html"

class SubscriptionView(generic.TemplateView):
    template_name = "sport/subscription.html"
