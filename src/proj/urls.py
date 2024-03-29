from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name='homepage/login_dj.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include('homepage.urls', namespace='homepage')),
    path("expences/", include('expences.urls'), name="expences"),
    path("notes/", include('notes.urls'), name="notes"),
    path("user/", include('user_register.urls'), name="user"),
    path("sport/", include('sport.urls'), name="sport")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)