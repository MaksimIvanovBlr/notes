from django.urls import reverse_lazy
from django.views import generic
from . import models, forms


class RegisterUser(generic.CreateView):
    form_class = forms.RegisterUserForm
    template_name = 'user_register/user_register.html'
    success_url = reverse_lazy('homepage:home')