from django.db import models


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


class PartnerApplication(models.Model):
    business_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=120)
    email = models.EmailField()
    location = models.CharField(max_length=120)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class VolunteerApplication(models.Model):
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    interest = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
