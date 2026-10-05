from django.core.management.base import BaseCommand
from booking.models import Facility, Resource

class Command(BaseCommand):
    help = "Create sample campus facilities and resources."

    def handle(self, *args, **options):
        facilities = [
            dict(name="Innovation Auditorium", code="AUD-01", facility_type="auditorium",
                 location="Main Block • Ground Floor", capacity=500,
                 description="Large event auditorium for seminars, conferences and campus ceremonies.",
                 amenities="Projector, Stage, PA System, Wi-Fi, Air Conditioning"),
            dict(name="Smart Classroom 204", code="CR-204", facility_type="classroom",
                 location="Academic Block A • 2nd Floor", capacity=60,
                 description="Technology-enabled classroom suitable for lectures, workshops and tutorials.",
                 amenities="Interactive Display, Projector, Wi-Fi, Whiteboard"),
            dict(name="Computer Lab 3", code="LAB-03", facility_type="lab",
                 location="Technology Block • 1st Floor", capacity=40,
                 description="Dedicated computing laboratory for practical sessions and technical workshops.",
                 amenities="40 PCs, LAN, Projector, UPS, Air Conditioning"),
            dict(name="Board Room", code="MR-01", facility_type="meeting",
                 location="Administration Block • 1st Floor", capacity=18,
                 description="Professional meeting room for committees, project reviews and staff meetings.",
                 amenities="Video Conference, Display, Whiteboard, Wi-Fi"),
            dict(name="Indoor Sports Hall", code="SP-01", facility_type="sports",
                 location="Sports Complex", capacity=120,
                 description="Multi-purpose indoor sports facility for training and campus events.",
                 amenities="Court, Scoreboard, Changing Rooms, Sound System"),
            dict(name="Seminar Room B", code="SEM-B", facility_type="meeting",
                 location="Library Block • 3rd Floor", capacity=35,
                 description="Quiet seminar space for group discussions and academic presentations.",
                 amenities="Projector, Wi-Fi, Whiteboard, Flexible Seating"),
        ]
        for data in facilities:
            Facility.objects.update_or_create(code=data["code"], defaults=data)

        resources = [
            ("Projector", "av", 12, 10, "Central Store"),
            ("Wireless Microphone", "av", 20, 18, "Central Store"),
            ("Laptop", "it", 30, 25, "IT Services"),
            ("Portable Speaker", "av", 8, 7, "Events Store"),
            ("Folding Table", "furniture", 40, 36, "Facilities Store"),
            ("Sports Kit", "sports", 15, 12, "Sports Complex"),
        ]
        for name, rtype, total, available, location in resources:
            Resource.objects.update_or_create(
                name=name,
                defaults=dict(resource_type=rtype, total_quantity=total,
                              available_quantity=available, location=location)
            )
        self.stdout.write(self.style.SUCCESS("Demo campus data created."))
