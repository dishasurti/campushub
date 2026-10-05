from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("facilities/", views.facilities, name="facilities"),
    path("facilities/<int:pk>/", views.facility_detail, name="facility_detail"),
    path("register/", views.register_view, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("book/", views.create_booking, name="create_booking"),
    path("bookings/<int:pk>/cancel/", views.cancel_booking, name="cancel_booking"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("bookings/<int:pk>/<str:action>/", views.booking_action, name="booking_action"),
]
