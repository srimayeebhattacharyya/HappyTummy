from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home_view, name='home'),

    path('auth-required/', views.auth_required_view, name='auth_required'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('donations/', include('donations.urls')),
]
