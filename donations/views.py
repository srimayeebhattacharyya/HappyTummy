from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import requests


from .models import (
    RestaurantProfile,
    VolunteerProfile,
    NGOProfile,
    SurplusFoodRequest,
    PickupTask,
    Donation,
)

from .forms import (
    RestaurantForm,
    VolunteerForm,
    NGOForm,
    DonationForm,
    SurplusFoodRequestForm,
)

# ===========================
# 1. RECENT DONATIONS (HOMEPAGE)
# ===========================
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


# ===========================
# 2. RESTAURANT REGISTRATION
# ===========================
@require_POST
def submit_restaurant(request):
    form = RestaurantForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({"status": "success"})
        except IntegrityError:
            form.add_error(None, "This restaurant profile already exists.")
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


# ===========================
# 3. VOLUNTEER REGISTRATION
# ===========================
@require_POST
def submit_volunteer(request):
    form = VolunteerForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({"status": "success"})
        except IntegrityError:
            form.add_error(None, "Volunteer already registered.")
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


# ===========================
# 4. NGO REGISTRATION
# ===========================
@require_POST
def submit_ngo(request):
    form = NGOForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({"status": "success"})
        except IntegrityError:
            form.add_error(None, "NGO already registered.")
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


# ===========================
# 5. DONATION FORM (OLD DATA)
# ===========================
@require_POST
def submit_donation(request):
    form = DonationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


# ===========================
# 6. SURPLUS FOOD CONFIRMATION
# ===========================
def surplus_form_page(request, restaurant_id):
    restaurant = get_object_or_404(RestaurantProfile, id=restaurant_id)

    if request.method == "POST":
        form = SurplusFoodRequestForm(request.POST)
        if form.is_valid():
            sr = form.save(commit=False)
            sr.restaurant = restaurant
            sr.save()
            return render(request, "surplus_success.html", {"restaurant": restaurant})

    return render(request, "surplus_confirm.html", {"restaurant": restaurant})

@require_POST
def confirm_surplus(request, restaurant_id):
    restaurant = get_object_or_404(RestaurantProfile, id=restaurant_id)
    form = SurplusFoodRequestForm(request.POST)

    if form.is_valid():
        sr = form.save(commit=False)
        sr.restaurant = restaurant
        sr.save()
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error", "errors": form.errors}, status=400)

@login_required(login_url="/")
def submit_surplus(request, profile_id):
    restaurant = get_object_or_404(RestaurantProfile, id=profile_id)

    if request.method == "POST":
        form = SurplusFoodRequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.restaurant = restaurant
            obj.save()
            return redirect("restaurant_dashboard")

    return redirect("restaurant_dashboard")

@login_required(login_url="/")
def restaurant_dashboard(request):
    profile = RestaurantProfile.objects.get(user=request.user)

    # -----------------------------
    # Geocode restaurant address → lat/lng
    # -----------------------------
    full_address = f"{profile.address}, {profile.city}"

    lat, lng = 22.5726, 88.3639  # fallback
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": full_address,
            "format": "json",
            "limit": 1
        }
        res = requests.get(url, params=params, headers={"User-Agent": "HappyTummy-App"})
        data = res.json()

        if data:
            lat = float(data[0]["lat"])
            lng = float(data[0]["lon"])
    except:
        pass

    # ---------------------------------------
    # Dashboard data (these MUST exist before return)
    # ---------------------------------------
    requests_qs = SurplusFoodRequest.objects.filter(restaurant=profile)

    total_donations = requests_qs.count()
    pending_pickups = requests_qs.filter(is_picked=False).count()
    completed_pickups = requests_qs.filter(is_picked=True).count()

    # ---------------------------------------
    # FINALLY — RETURN RENDER HERE!
    # ---------------------------------------
    return render(request, "dashboard/restaurant_dashboard.html", {
        "profile": profile,
        "requests": requests_qs,
        "total_donations": total_donations,
        "pending_pickups": pending_pickups,
        "completed_pickups": completed_pickups,
        "lat": lat,
        "lng": lng,
    })