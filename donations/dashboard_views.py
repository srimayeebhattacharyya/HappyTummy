from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from donations.models import (
    RestaurantProfile,
    VolunteerProfile,
    NGOProfile,
    SurplusFoodRequest,
    PickupTask,
)


# ---------------------------
# RESTAURANT DASHBOARD
# ---------------------------
@login_required(login_url="/")
def restaurant_dashboard(request):
    profile = RestaurantProfile.objects.get(user=request.user)

    # --------------------------
    # HANDLE POST (FORMS)
    # --------------------------
    if request.method == "POST":
        action = request.POST.get("action")

        # 1) Add new donation
        if action == "add_donation":
            food_type = request.POST.get("food_type")
            quantity = request.POST.get("quantity")

            SurplusFoodRequest.objects.create(
                restaurant=profile,
                food_type=food_type,
                quantity=quantity,
            )
            return redirect("restaurant_dashboard")

        # 2) Update profile
        elif action == "update_profile":
            profile.business_name = request.POST.get("business_name")
            profile.contact_person = request.POST.get("contact_person")
            profile.phone = request.POST.get("phone")
            profile.city = request.POST.get("city")
            profile.address = request.POST.get("address")
            profile.save()
            return redirect("restaurant_dashboard")

    # --------------------------
    # LOAD DASHBOARD DATA (GET)
    # --------------------------
    requests = SurplusFoodRequest.objects.filter(restaurant=profile)

    total_donations = requests.count()
    pending_pickups = requests.filter(is_picked=False).count()
    completed_pickups = requests.filter(is_picked=True).count()

    return render(request, "dashboard/restaurant_dashboard.html", {
        "profile": profile,
        "requests": requests,
        "total_donations": total_donations,
        "pending_pickups": pending_pickups,
        "completed_pickups": completed_pickups,
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
