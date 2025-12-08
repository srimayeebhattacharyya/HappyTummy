from django.db import models


# ============================
# 1. RESTAURANT PARTNER MODEL
# ============================
import uuid
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=200, unique=True)
    contact_person = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
# ============================
# 2. NGO MODEL
# ============================
class NGO(models.Model):
    name = models.CharField(max_length=200, unique=True)
    contact_person = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


# ============================
# 3. VOLUNTEER MODEL
# ============================
class Volunteer(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    area = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.full_name


# ============================
# 4. SURPLUS FOOD REQUEST
# ============================
class SurplusFoodRequest(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    food_type = models.CharField(max_length=120)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_picked = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.restaurant.name} - {self.quantity} meals"


# ============================
# 5. PICKUP ASSIGNMENT
# ============================
class PickupTask(models.Model):
    request = models.ForeignKey(SurplusFoodRequest, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Volunteer, on_delete=models.SET_NULL, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"Pickup for: {self.request.restaurant.name}"


# ============================
# 6. OLD DONATION MODEL (KEEPING FOR ANALYTICS)
# ============================
class Donation(models.Model):
    restaurant_name = models.CharField(max_length=200)
    food_type = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField()
    city = models.CharField(max_length=120)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.restaurant_name} - {self.quantity} meals"

from django.contrib.auth.models import User
class RestaurantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.business_name
    
class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, unique=True)
    area = models.CharField(max_length=150)
    is_available = models.BooleanField(default=True)   # volunteer availability toggle

    def __str__(self):
        return self.full_name

class NGOProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    ROLE_CHOICES = (
        ("restaurant", "Restaurant"),
        ("volunteer", "Volunteer"),
        ("ngo", "NGO"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} — {self.role}"
