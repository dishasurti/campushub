from django.contrib import admin
from .models import Facility, Resource, Booking, BookingResource

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "facility_type", "location", "capacity", "is_active")
    list_filter = ("facility_type", "is_active")
    search_fields = ("name", "code", "location")

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "resource_type", "total_quantity", "available_quantity", "condition")
    list_filter = ("resource_type", "is_active")
    search_fields = ("name",)

class BookingResourceInline(admin.TabularInline):
    model = BookingResource
    extra = 0

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("facility", "user", "booking_date", "start_time", "end_time", "status")
    list_filter = ("status", "booking_date")
    search_fields = ("facility__name", "facility__code", "user__username", "purpose")
    list_editable = ("status",)
    inlines = [BookingResourceInline]

@admin.register(BookingResource)
class BookingResourceAdmin(admin.ModelAdmin):
    list_display = ("booking", "resource", "quantity")
