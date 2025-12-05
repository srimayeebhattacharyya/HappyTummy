from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Donation
from donations.forms import PartnerForm, VolunteerForm, DonationForm

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


@require_POST
def submit_partner(request):
    form = PartnerForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@require_POST
def submit_volunteer(request):
    form = VolunteerForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@require_POST
def submit_donation(request):
    form = DonationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)
