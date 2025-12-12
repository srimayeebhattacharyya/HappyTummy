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
    # HANDLE POST REQUESTS (donation + profile update)
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
            profile.city = request.POST.get("city")
            profile.address = request.POST.get("address")
            profile.save()
            return redirect("restaurant_dashboard")


    # CLEAN & NORMALIZE ADDRESS
    import re

    raw_address = f"{profile.address} {profile.city}".strip()
    clean_address = re.sub(r"\s+", " ", raw_address)  # remove newlines + extra spaces

    # Normalize city spellings
    city_lower = profile.city.strip().lower()
    if city_lower in ["srirampur", "srerampur", "shrirampur", "srirampore"]:
        normalized_city = "Serampore"
    else:
        normalized_city = profile.city.strip()

    # Detect postal code in address
    address_text = f"{profile.address} {profile.city}"
    postal = None
    m = re.search(r"(\d{6})", address_text)
    if m:
        postal = m.group(1)
        print("PIN FOUND:", postal)
    else:
        postal = ""
        print("NO PIN FOUND in:", address_text)

    # Build final geocoder address
    if postal:
        full_address = f"{normalized_city}, Hooghly, West Bengal, {postal}, India"
    else:
        full_address = f"{clean_address}, {normalized_city}, Hooghly, West Bengal, India"

    print("\n============================")
    print(" FINAL ADDRESS SENT TO API:")
    print(full_address)
    print("============================\n")

    # -----------------------------
    # GEOCODING
    # -----------------------------
    lat = lng = None
    data = None

    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": full_address, "format": "json", "limit": 1}
        headers = {"User-Agent": "HappyTummy-App"}

        res = requests.get(url, params=params, headers=headers, timeout=5)
        data = res.json()

        print("RAW RESPONSE FROM API:", data)

        if data:
            lat = float(data[0]["lat"])
            lng = float(data[0]["lon"])
            print("✔ Parsed LAT/LNG:", lat, lng)
        else:
            print("❌ API returned EMPTY list")

    except Exception as e:
        print("❌ GEOCODING ERROR:", e)

    # -----------------------------
    # FALLBACK
    # -----------------------------
    if not lat or not lng:
        print("⚠ FALLBACK to Kolkata")
        lat, lng = 22.5726, 88.3639


    # -----------------------------
    # DASHBOARD DATA
    # -----------------------------
    requests_qs = SurplusFoodRequest.objects.filter(restaurant=profile)

    return render(
        request,
        "dashboard/restaurant_dashboard.html",
        {
            "profile": profile,
            "requests": requests_qs,
            "total_donations": requests_qs.count(),
            "pending_pickups": requests_qs.filter(is_picked=False).count(),
            "completed_pickups": requests_qs.filter(is_picked=True).count(),
            "lat": lat,
            "lng": lng,
        },
    )

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
