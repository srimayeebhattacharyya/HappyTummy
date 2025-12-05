from django.contrib import admin
from .models import Donation, PartnerApplication, VolunteerApplication

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("restaurant_name", "food_type", "quantity", "city", "date")
    search_fields = ("restaurant_name", "food_type", "city")
    list_filter = ("city", "date")

@admin.register(PartnerApplication)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("business_name", "contact_person", "email", "location", "created_at")
    search_fields = ("business_name", "contact_person", "email", "location")
    list_filter = ("location", "created_at")

@admin.register(VolunteerApplication)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "created_at")
    search_fields = ("full_name", "email", "phone")
    list_filter = ("created_at",)
