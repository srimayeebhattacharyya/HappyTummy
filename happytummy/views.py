from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# =======================
# HOME PAGE
# =======================
def home_view(request):
    return render(request, "index.html")


# =======================
# AUTH REQUIRED PAGE
# =======================
def auth_required_view(request):
    return render(request, "auth_required.html")


# =======================
# LOGIN PAGE
# =======================
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("/dashboard/")
        else:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


# =======================
# REGISTER PAGE
# =======================
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        p1 = request.POST.get("password1")
        p2 = request.POST.get("password2")

        if p1 != p2:
            return render(request, "register.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already taken"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {
                "error": "Email already registered"
            })

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=p1
        )
        return redirect("/login/")

    return render(request, "register.html")


# =======================
# DASHBOARD PAGE
# =======================
@login_required(login_url="/auth-required/")
def dashboard_view(request):
    return render(request, "dashboard.html")