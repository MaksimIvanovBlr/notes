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


    path("create-subscription-visit", views.SubscriptionVisitCreateView.as_view(), name="create-subscription-visit"),
    path("list-subscription-visit/", views.SubscriptionVisitListView.as_view(), name="list-subscription-visit"),
    path("update-subscription-visit/<int:pk>", views.SubscriptionVisitUpdateView.as_view(), name="update-subscription-visit"),
    path("delete-subscription-visit/<int:pk>", views.SubscriptionVisitDeleteView.as_view(), name="delete-subscription-visit"),

]
