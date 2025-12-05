from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.donation_list, name="donation_list"),
    path("submit-partner/", views.submit_partner, name="submit_partner"),
    path("submit-volunteer/", views.submit_volunteer, name="submit_volunteer"),
    path("submit-donation/", views.submit_donation, name="submit_donation"),
]
