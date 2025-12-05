from django import forms
from .models import Donation, PartnerApplication, VolunteerApplication

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ["restaurant_name", "food_type", "quantity", "city"]

class PartnerForm(forms.ModelForm):
    class Meta:
        model = PartnerApplication
        fields = ["business_name", "contact_person", "email", "location", "message"]

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ["full_name", "email", "phone", "interest"]
