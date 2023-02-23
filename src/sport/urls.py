from django.urls import path
from . import views

app_name = "sport"

urlpatterns = [
    path("", views.HomepageView.as_view(), name="main"),

    path("subscription/", views.SubscriptionView.as_view(), name="subscription"),
    path("create-subscription", views.SubscriptionCreateView.as_view(), name="create-subscription"),
    path("list-subscription/", views.SubscriptionListView.as_view(), name="list-subscription"),
    path("update-subscription/<int:pk>", views.SubscriptionUpdateView.as_view(), name="update-subscription"),
    path("detail-subscription/<int:pk>", views.SubscriptionDetailView.as_view(), name="detail-subscription"),
    path("delete-subscription/<int:pk>", views.SubscriptionDeleteView.as_view(), name="delete-subscription"),


    # path("subscription/", views.SubscriptionView.as_view(), name="subscription"),
    # path("create-subscription", views.SubscriptionCreateView.as_view(), name="create-subscription"),
    # path("list-subscription/", views.SubscriptionListView.as_view(), name="list-subscription"),
    # path("update-subscription/<int:pk>", views.SubscriptionUpdateView.as_view(), name="update-subscription"),
    # path("detail-subscription/<int:pk>", views.SubscriptionDetailView.as_view(), name="detail-subscription"),
    # path("delete-subscription/<int:pk>", views.SubscriptionDeleteView.as_view(), name="delete-subscription"),

]
