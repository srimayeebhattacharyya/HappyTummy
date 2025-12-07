from django import forms
from .models import (
    Restaurant,
    Volunteer,
    NGO,
    Donation,
    SurplusFoodRequest,
)


# ============ RESTAURANT REGISTRATION FORM ============
class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ["name", "contact_person", "email", "phone", "city", "address"]


# ============ VOLUNTEER REGISTRATION FORM ============
class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ["full_name", "email", "phone", "area"]


# ============ NGO REGISTRATION FORM ============
class NGOForm(forms.ModelForm):
    class Meta:
        model = NGO
        fields = ["name", "contact_person", "email", "phone", "address", "city"]


# ============ OLD DONATION FORM (KEEP) ============
class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ["restaurant_name", "food_type", "quantity", "city"]


# ============ SURPLUS FOOD CONFIRMATION FORM ============
class SurplusFoodRequestForm(forms.ModelForm):
    class Meta:
        model = SurplusFoodRequest
        fields = ["food_type", "quantity"]
