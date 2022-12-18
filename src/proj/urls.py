from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('homepage.urls', namespace='homepage')),
    path("budgeting/", include('budgeting.urls', namespace='budgeting')),
    path("expences/", include('expences.urls'), name="expences"),
    path("notes/", include('notes.urls'), name="notes")
]
