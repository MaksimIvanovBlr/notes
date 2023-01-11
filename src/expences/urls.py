from django.urls import path
from . import views

app_name = 'expences'

urlpatterns = [
    path("create", views.CreateExpences.as_view(), name="create"),
    path("update/<int:pk>", views.UpdateExpences.as_view(), name="update"),
    path("detail/<int:pk>", views.DetailExpences.as_view(), name="detail"),
    path("delete/<int:pk>", views.DeleteExpences.as_view(), name="delete"),
    path("list/", views.ListExpences.as_view(), name="list"),
    # path("", views.ExpencesView.as_view(), name="main"),
    path("", views.expences_view, name="main"),
    path("recalculation/", views.recalculation, name="recalculation"),

    path("create-s", views.CreateIncome.as_view(), name="create-s"),
    path("update-s/<int:pk>", views.UpdateIncome.as_view(), name="update-s"),
    path("detail-s/<int:pk>", views.DetailIncome.as_view(), name="detail-s"),
    path("delete-s/<int:pk>", views.DeleteIncome.as_view(), name="delete-s"),
    path("list-s/", views.ListIncome.as_view(), name="list-s"),

    path("create-per-day", views.CreatePerDay.as_view(), name="create-per-day"),
    path("update-per-day/<int:pk>", views.UpdatePerDay.as_view(), name="update-per-day"),

    path("reserv/<int:pk>", views.UpdateReserv.as_view(), name="reserv"),

    path("create-a/", views.CreateAdditional.as_view(), name="create-a"),
    path("update-a/<int:pk>", views.UpdateAdditional.as_view(), name="update-a"),
    path("delete-a/<int:pk>", views.DeleteAdditional.as_view(), name="delete-a"),
    path("list-a/", views.ListAdditional.as_view(), name="list-a")
]
