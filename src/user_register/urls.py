from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path("user-register/", views.RegisterUser.as_view(), name="user-register"),
]
