from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from .models import Donation, Restaurant, SurplusFoodRequest
from .forms import (
    RestaurantForm,
    VolunteerForm,
    NGOForm,
    DonationForm,
    SurplusFoodRequestForm,
)


# ======================
# 1. HOMEPAGE DONATION LIST (for "Recent Donations" section)
# ======================
def donation_list(request):
    qs = Donation.objects.all()[:15]
    data = [
        {
            "restaurant_name": d.restaurant_name,
            "food_type": d.food_type,
            "quantity": d.quantity,
            "city": d.city,
            "date": d.date.strftime("%d %b %Y"),
        }
        for d in qs
    ]
    return JsonResponse(data, safe=False)


# ======================
# 2. RESTAURANT REGISTRATION
# (Form action: /donations/submit-restaurant/)
# ======================
@require_POST
def submit_restaurant(request):
    form = RestaurantForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({"status": "success"})
        except IntegrityError:
            # Same restaurant/email/phone already exists
            form.add_error(None, "This restaurant is already registered with us.")
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


# ======================
# 3. VOLUNTEER REGISTRATION
# (Form action: /donations/submit-volunteer/)
# ======================
@require_POST
def submit_volunteer(request):
    form = VolunteerForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({"status": "success"})
        except IntegrityError:
            form.add_error(None, "You are already registered as a volunteer.")
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


# ======================
# 4. NGO REGISTRATION
# (Form action: /donations/submit-ngo/)
# ======================
@require_POST
def submit_ngo(request):
    form = NGOForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({"status": "success"})
        except IntegrityError:
            form.add_error(None, "This NGO is already registered with us.")
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


# ======================
# 5. OLD DONATION (KEEP FOR ANALYTICS / DASHBOARD)
# ======================
@require_POST
def submit_donation(request):
    form = DonationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


# ======================
# 6. SURPLUS FOOD CONFIRMATION
# (Used when restaurant clicks "YES, we have food" link/button)
# ======================
@require_POST
def confirm_surplus(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    form = SurplusFoodRequestForm(request.POST)

    if form.is_valid():
        sr = form.save(commit=False)
        sr.restaurant = restaurant
        sr.save()
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error", "errors": form.errors}, status=400)
from django.shortcuts import render

def surplus_form_page(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        form = SurplusFoodRequestForm(request.POST)
        if form.is_valid():
            sr = form.save(commit=False)
            sr.restaurant = restaurant
            sr.save()
            return render(request, "surplus_success.html", {"restaurant": restaurant})

    return render(request, "surplus_confirm.html", {"restaurant": restaurant})
