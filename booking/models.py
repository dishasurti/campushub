from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class Facility(models.Model):
    FACILITY_TYPES = [
        ("classroom", "Classroom"),
        ("lab", "Laboratory"),
        ("auditorium", "Auditorium"),
        ("sports", "Sports"),
        ("meeting", "Meeting Room"),
        ("library", "Library Space"),
    ]
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=30, unique=True)
    facility_type = models.CharField(max_length=30, choices=FACILITY_TYPES)
    location = models.CharField(max_length=150)
    capacity = models.PositiveIntegerField(default=10)
    description = models.TextField(blank=True)
    amenities = models.CharField(max_length=500, blank=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Resource(models.Model):
    RESOURCE_TYPES = [
        ("equipment", "Equipment"),
        ("furniture", "Furniture"),
        ("av", "AV Equipment"),
        ("it", "IT Device"),
        ("sports", "Sports Equipment"),
    ]
    name = models.CharField(max_length=120)
    resource_type = models.CharField(max_length=30, choices=RESOURCE_TYPES)
    total_quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=120, blank=True)
    condition = models.CharField(max_length=120, default="Good")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="bookings")
    purpose = models.CharField(max_length=200)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    attendees = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-booking_date", "-start_time"]

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be later than start time.")
        if self.attendees > self.facility.capacity:
            raise ValidationError("Attendee count exceeds facility capacity.")

        overlapping = Booking.objects.filter(
            facility=self.facility,
            booking_date=self.booking_date,
            status__in=["pending", "approved"],
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)
        if overlapping.exists():
            raise ValidationError("This facility is already requested/booked for that time.")

    def __str__(self):
        return f"{self.facility.code} - {self.booking_date} - {self.user.username}"


class BookingResource(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="resources")
    resource = models.ForeignKey(Resource, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("booking", "resource")

    def clean(self):
        if self.quantity < 1:
            raise ValidationError("Quantity must be at least 1.")
