# Campus Facility Booking & Resource Management

A complete Django starter website for managing campus facilities, room bookings,
equipment/resources, approvals, and an admin dashboard.

## Features
- Student/staff registration and login
- Facility directory with capacity, location, amenities and availability
- Booking request workflow
- Conflict prevention for overlapping approved/pending bookings
- My bookings page with cancellation
- Admin dashboard with booking approval/rejection
- Resource inventory and resource allocation per booking
- Django admin for managing all data
- Responsive modern UI

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

The demo command creates sample facilities/resources. You can register a normal
user from the website, then use the Django admin to promote a user to staff.
