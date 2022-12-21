from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class HomepageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'homepage/homepage.html'
    login_url = reverse_lazy('login')
