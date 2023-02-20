from django.urls import path
from . import views

app_name = "sport"

urlpatterns = [
    path("", views.HomepageView.as_view(), name="main"),

    path("subscription/", views.SubscriptionView.as_view(), name="subscription"),
]
