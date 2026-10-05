from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import BookingForm, RegisterForm
from .models import Booking, Facility, Resource


def home(request):
    facilities = Facility.objects.filter(is_active=True)[:6]
    return render(request, "booking/home.html", {
        "facilities": facilities,
        "facility_count": Facility.objects.filter(is_active=True).count(),
        "resource_count": Resource.objects.filter(is_active=True).count(),
        "booking_count": Booking.objects.filter(status="approved").count(),
    })


def facilities(request):
    qs = Facility.objects.filter(is_active=True)
    q = request.GET.get("q", "").strip()
    facility_type = request.GET.get("type", "").strip()
    if q:
        qs = qs.filter(name__icontains=q) | qs.filter(location__icontains=q) | qs.filter(code__icontains=q)
    if facility_type:
        qs = qs.filter(facility_type=facility_type)
    return render(request, "booking/facilities.html", {
        "facilities": qs.distinct(),
        "types": Facility.FACILITY_TYPES,
        "selected_type": facility_type,
        "q": q,
    })


def facility_detail(request, pk):
    facility = get_object_or_404(Facility, pk=pk, is_active=True)
    upcoming = facility.bookings.filter(status="approved").order_by("booking_date", "start_time")[:8]
    return render(request, "booking/facility_detail.html", {"facility": facility, "upcoming": upcoming})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    bookings = request.user.bookings.select_related("facility").all()[:10]
    stats = {
        "total": request.user.bookings.count(),
        "pending": request.user.bookings.filter(status="pending").count(),
        "approved": request.user.bookings.filter(status="approved").count(),
    }
    return render(request, "booking/dashboard.html", {"bookings": bookings, "stats": stats})


@login_required
def create_booking(request):
    form = BookingForm(request.POST or None)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        try:
            booking.full_clean()
            booking.save()
            messages.success(request, "Booking request submitted for approval.")
            return redirect("dashboard")
        except Exception as exc:
            form.add_error(None, str(exc))
    return render(request, "booking/booking_form.html", {"form": form})


@login_required
@require_POST
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status in ["pending", "approved"]:
        booking.status = "cancelled"
        booking.save(update_fields=["status", "updated_at"])
        messages.success(request, "Booking cancelled.")
    return redirect("dashboard")


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def admin_dashboard(request):
    bookings = Booking.objects.select_related("facility", "user").all()[:20]
    context = {
        "bookings": bookings,
        "pending": Booking.objects.filter(status="pending").count(),
        "approved": Booking.objects.filter(status="approved").count(),
        "facilities": Facility.objects.filter(is_active=True).count(),
        "resources": Resource.objects.filter(is_active=True).count(),
    }
    return render(request, "booking/admin_dashboard.html", context)


@user_passes_test(is_staff)
@require_POST
def booking_action(request, pk, action):
    booking = get_object_or_404(Booking, pk=pk)
    if action == "approve":
        try:
            booking.status = "approved"
            booking.full_clean()
            booking.save(update_fields=["status", "updated_at"])
            messages.success(request, "Booking approved.")
        except Exception as exc:
            messages.error(request, f"Cannot approve: {exc}")
    elif action == "reject":
        booking.status = "rejected"
        booking.admin_note = request.POST.get("admin_note", "")
        booking.save(update_fields=["status", "admin_note", "updated_at"])
        messages.success(request, "Booking rejected.")
    return redirect("admin_dashboard")
