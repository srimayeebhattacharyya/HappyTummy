from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

from donations.models import (
    UserRole,
    RestaurantProfile,
    VolunteerProfile,
    NGOProfile
)

# ==========================================
# RESTAURANT REGISTER
# ==========================================
def restaurant_register(request):
    if request.method == "POST":
        u = request.POST["username"]
        e = request.POST["email"]
        p1 = request.POST["password1"]
        p2 = request.POST["password2"]

        if p1 != p2:
            return render(request, "auth/restaurant_register.html",
                          {"error": "Passwords do not match"})

        if User.objects.filter(username=u).exists():
            return render(request, "auth/restaurant_register.html",
                          {"error": "Username already taken"})

        if User.objects.filter(email=e).exists():
            return render(request, "auth/restaurant_register.html",
                          {"error": "Email already registered"})

        user = User.objects.create_user(username=u, email=e, password=p1)

        # Assign role
        UserRole.objects.create(user=user, role="restaurant")

        # Create empty profile
        RestaurantProfile.objects.create(
            user=user,
            business_name="",
            contact_person="",
            phone="",
            city="",
            address=""
        )

        login(request, user)
        return redirect("/dashboard/")

    return render(request, "auth/restaurant_register.html")


# ==========================================
# RESTAURANT LOGIN
# ==========================================
def restaurant_login(request):
    if request.method == "POST":
        u = request.POST["username"]
        p = request.POST["password"]

        user = authenticate(request, username=u, password=p)

        if not user:
            return render(request, "auth/restaurant_login.html",
                          {"error": "Invalid username or password"})

        # Verify role
        if not hasattr(user, "userrole") or user.userrole.role != "restaurant":
            return render(request, "auth/restaurant_login.html",
                          {"error": "This is not a restaurant account"})

        login(request, user)
        return redirect("/dashboard/")

    return render(request, "auth/restaurant_login.html")

def volunteer_register(request):
    if request.method == "POST":
        u = request.POST["username"]
        e = request.POST["email"]
        p1 = request.POST["password1"]
        p2 = request.POST["password2"]

        if p1 != p2:
            return render(request, "auth/volunteer_register.html",
                          {"error": "Passwords do not match"})

        if User.objects.filter(username=u).exists():
            return render(request, "auth/volunteer_register.html",
                          {"error": "Username already taken"})

        if User.objects.filter(email=e).exists():
            return render(request, "auth/volunteer_register.html",
                          {"error": "Email already registered"})

        # Create USER
        user = User.objects.create_user(username=u, email=e, password=p1)

        # Assign ROLE
        UserRole.objects.create(user=user, role="volunteer")

        # Create volunteer profile
        VolunteerProfile.objects.create(
            user=user,
            full_name="",
            phone="",
            area=""
        )

        login(request, user)
        return redirect("/dashboard/")

    return render(request, "auth/volunteer_register.html")

def volunteer_login(request):
    if request.method == "POST":
        u = request.POST["username"]
        p = request.POST["password"]

        user = authenticate(request, username=u, password=p)

        if not user:
            return render(request, "auth/volunteer_login.html",
                          {"error": "Invalid username or password"})

        if not hasattr(user, "userrole") or user.userrole.role != "volunteer":
            return render(request, "auth/volunteer_login.html",
                          {"error": "This account is not a Volunteer account"})

        login(request, user)
        return redirect("/dashboard/")

    return render(request, "auth/volunteer_login.html")

def ngo_register(request):
    if request.method == "POST":
        u = request.POST["username"]
        e = request.POST["email"]
        p1 = request.POST["password1"]
        p2 = request.POST["password2"]

        if p1 != p2:
            return render(request, "auth/ngo_register.html",
                          {"error": "Passwords do not match"})

        if User.objects.filter(username=u).exists():
            return render(request, "auth/ngo_register.html",
                          {"error": "Username already taken"})

        if User.objects.filter(email=e).exists():
            return render(request, "auth/ngo_register.html",
                          {"error": "Email already registered"})

        user = User.objects.create_user(username=u, email=e, password=p1)

        UserRole.objects.create(user=user, role="ngo")

        NGOProfile.objects.create(
            user=user,
            name="",
            contact_person="",
            phone="",
            address="",
            city=""
        )

        login(request, user)
        return redirect("/dashboard/")

    return render(request, "auth/ngo_register.html")

def ngo_login(request):
    if request.method == "POST":
        u = request.POST["username"]
        p = request.POST["password"]

        user = authenticate(request, username=u, password=p)

        if not user:
            return render(request, "auth/ngo_login.html",
                          {"error": "Invalid username or password"})

        if not hasattr(user, "userrole") or user.userrole.role != "ngo":
            return render(request, "auth/ngo_login.html",
                          {"error": "This account is not an NGO account"})

        login(request, user)
        return redirect("/dashboard/")

    return render(request, "auth/ngo_login.html")

# ==========================================
# DASHBOARD REDIRECTOR
# ==========================================
@login_required(login_url="/")   # if NOT logged in → redirect to homepage
def dashboard_redirect(request):
    """Send logged-in user to the correct dashboard based on role."""

    role = request.user.userrole.role  # get assigned role

    if role == "restaurant":
        return redirect("/dashboard/restaurant/")

    elif role == "volunteer":
        return redirect("/dashboard/volunteer/")

    elif role == "ngo":
        return redirect("/dashboard/ngo/")

    # fallback in case role missing
    return redirect("/")

def logout_view(request):
    logout(request)
    return redirect("/")