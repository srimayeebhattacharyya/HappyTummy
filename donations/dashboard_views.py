from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from donations.models import (
    RestaurantProfile,
    VolunteerProfile,
    NGOProfile,
    SurplusFoodRequest,
    PickupTask,
)
import requests
# ---------------------------
# RESTAURANT DASHBOARD
# ---------------------------
@login_required(login_url="/")
def restaurant_dashboard(request):
    profile = RestaurantProfile.objects.get(user=request.user)

    # -------------------------------------------------
    # HANDLE POST REQUESTS
    # -------------------------------------------------
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_donation":
            SurplusFoodRequest.objects.create(
                restaurant=profile,
                food_type=request.POST.get("food_type"),
                quantity=request.POST.get("quantity"),
            )
            return redirect("restaurant_dashboard")

        elif action == "update_profile":
            profile.business_name = request.POST.get("business_name")
            profile.contact_person = request.POST.get("contact_person")
            profile.phone = request.POST.get("phone")

            profile.state = request.POST.get("state")
            profile.district = request.POST.get("district")
            profile.city = request.POST.get("city")

            profile.address = request.POST.get("address")

            profile.save()
            return redirect("restaurant_dashboard")

    # -------------------------------------------------
    # GEOCODING (STRUCTURED — NO OCEAN)
    # -------------------------------------------------
    lat = lng = None

    try:
        params = {
            "street": profile.address,
            "city": profile.city,
            "state": profile.state,
            "postalcode": profile.pincode,
            "country": "India",
            "format": "json",
            "limit": 1,
        }

        res = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params=params,
            headers={"User-Agent": "HappyTummy-App"},
            timeout=8,
        )

        data = res.json()
        print("GEOCODER RESPONSE:", data)

        if data:
            lat = float(data[0]["lat"])
            lng = float(data[0]["lon"])

    except Exception as e:
        print("GEOCODING ERROR:", e)

    # -------------------------------------------------
    # FALLBACK (ONLY IF API FAILS)
    # -------------------------------------------------
    if not lat or not lng:
        lat, lng = 22.5726, 88.3639  # Kolkata

    # -------------------------------------------------
    # DASHBOARD DATA
    # -------------------------------------------------
    requests_qs = SurplusFoodRequest.objects.filter(restaurant=profile)

    total_donations = requests_qs.count()
    pending_pickups = requests_qs.filter(is_picked=False).count()
    completed_pickups = requests_qs.filter(is_picked=True).count()

    # -------------------------------------------------
    # RENDER
    # -------------------------------------------------
    return render(request, "dashboard/restaurant_dashboard.html", {
        "profile": profile,
        "requests": requests_qs,
        "total_donations": total_donations,
        "pending_pickups": pending_pickups,
        "completed_pickups": completed_pickups,
        "lat": lat,
        "lng": lng,
    })

# ---------------------------
# VOLUNTEER DASHBOARD
# ---------------------------
@login_required(login_url="/")
def volunteer_dashboard(request):
    profile = VolunteerProfile.objects.get(user=request.user)

    my_tasks = PickupTask.objects.filter(assigned_to=profile)

    return render(request, "dashboard/volunteer_dashboard.html", {
        "profile": profile,
        "tasks": my_tasks,
    })


# ---------------------------
# NGO DASHBOARD
# ---------------------------
@login_required(login_url="/")
def ngo_dashboard(request):
    profile = NGOProfile.objects.get(user=request.user)

    return render(request, "dashboard/ngo_dashboard.html", {
        "profile": profile,
    })
