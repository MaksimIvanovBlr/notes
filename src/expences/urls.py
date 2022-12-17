from django.urls import path
from . import views

app_name = 'expences'

urlpatterns = [
    path("create",views.CreateExpences.as_view(), name="create"),
    path("update/<int:pk>", views.UpdateExpences.as_view(), name="update"),
    path("detail/<int:pk>", views.DetailExpences.as_view(), name="detail"),
    path("delete/<int:pk>", views.DeleteExpences.as_view(), name="delete"),
    path("list/", views.ListExpences.as_view(), name="list"),
    path("", views.ExpencesView.as_view(), name="main")
]
