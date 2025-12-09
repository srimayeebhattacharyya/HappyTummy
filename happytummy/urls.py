from django.contrib import admin
from django.urls import path, include
from . import views
from donations import auth_views
from donations import dashboard_views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home_view, name='home'),

    path('auth-required/', views.auth_required_view, name='auth_required'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('donations/', include('donations.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ HOMEPAGE (add this back!)
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # ✅ Authentication routes
    path("restaurant/login/", auth_views.restaurant_login, name="restaurant_login"),
    path("restaurant/register/", auth_views.restaurant_register, name="restaurant_register"),

    path("volunteer/login/", auth_views.volunteer_login, name="volunteer_login"),
    path("volunteer/register/", auth_views.volunteer_register, name="volunteer_register"),

    path("ngo/login/", auth_views.ngo_login, name="ngo_login"),
    path("ngo/register/", auth_views.ngo_register, name="ngo_register"),

    path("logout/", auth_views.logout_view, name="logout"),

    path("dashboard/", auth_views.dashboard_redirect, name="dashboard_redirect"),

    path("dashboard/restaurant/", dashboard_views.restaurant_dashboard, name="restaurant_dashboard"),
    path("dashboard/volunteer/", dashboard_views.volunteer_dashboard, name="volunteer_dashboard"),
    path("dashboard/ngo/", dashboard_views.ngo_dashboard, name="ngo_dashboard"),


    # Include donations app URLs
    path("donations/", include("donations.urls")),
]
