from django.urls import path
from . import views

app_name = 'expences'

urlpatterns = [
    path("create",views.CreateExpences.as_view(), name="create"),
    path("update/<int:pk>", views.UpdateExpences.as_view(), name="update"),
    path("detail/<int:pk>", views.DetailExpences.as_view(), name="detail"),
    path("delete/<int:pk>", views.DeleteExpences.as_view(), name="delete"),
    path("list/", views.ListExpences.as_view(), name="list"),
    path("", views.ExpencesView.as_view(), name="main"),


    path("create-s",views.CreateIncome.as_view(), name="create-s"),
    path("update-s/<int:pk>", views.UpdateIncome.as_view(), name="update-s"),
    path("detail-s/<int:pk>", views.DetailIncome.as_view(), name="detail-s"),
    path("delete-s/<int:pk>", views.DeleteIncome.as_view(), name="delete-s"),
    path("list-s/", views.ListIncome.as_view(), name="list-s"),
]
