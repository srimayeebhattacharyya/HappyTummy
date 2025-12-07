from django.contrib import admin
from .models import (
    Restaurant,
    NGO,
    Volunteer,
    SurplusFoodRequest,
    PickupTask,
    Donation,
)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person", "email", "phone", "city", "created_at")
    search_fields = ("name", "email", "phone", "city")
    list_filter = ("city",)
    ordering = ("-created_at",)


@admin.register(NGO)
class NGOAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_person", "email", "phone", "city", "created_at")
    search_fields = ("name", "email", "phone", "city")
    list_filter = ("city",)
    ordering = ("-created_at",)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "area", "created_at")
    search_fields = ("full_name", "email", "phone", "area")
    list_filter = ("area",)
    ordering = ("-created_at",)


@admin.register(SurplusFoodRequest)
class SurplusFoodRequestAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "food_type", "quantity", "timestamp", "is_picked")
    search_fields = ("restaurant__name", "food_type")
    list_filter = ("is_picked", "timestamp")
    ordering = ("-timestamp",)


@admin.register(PickupTask)
class PickupTaskAdmin(admin.ModelAdmin):
    list_display = ("request", "assigned_to", "assigned_at", "completed")
    search_fields = ("request__restaurant__name", "assigned_to__full_name")
    list_filter = ("completed",)
    ordering = ("-assigned_at",)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("restaurant_name", "food_type", "quantity", "city", "date")
    search_fields = ("restaurant_name", "food_type", "city")
    list_filter = ("city", "food_type")
    ordering = ("-date",)
