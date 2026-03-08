from frontend.models import Event, EventStatistic, EventPartner, EventTeamMetric, EventImpact
from django.utils import timezone
import datetime

# Create the main event
event = Event.objects.create(
    title="Gbaremu Evangelical Outreach",
    description="An evangelical outreach was conducted at Gbaremu, Ibadan on November 26, 2025, organized by Optimizing People Evangelical Outreach in collaboration with ministry partners and volunteers. The program focused on proclaiming the Gospel of Jesus Christ while extending compassion and care to vulnerable members of the community.\n\nDuring the outreach, the message of salvation was preached with clarity and power, resulting in a strong spiritual response. A total of 48 individuals gave their lives to Christ, and 52 widows were identified for welfare support, reflecting the ministry's commitment to holistic outreach that addresses both spiritual and social needs.",
    date=timezone.make_aware(datetime.datetime(2025, 11, 26, 9, 0, 0)),
    location="Gbaremu, Ibadan, Nigeria",
    event_type="crusade",
    is_featured=True
)

# Create Event Statistics
EventStatistic.objects.create(event=event, value="89", label="Total Attendance", order=1)
EventStatistic.objects.create(event=event, value="52", label="Widows Support", order=2)
EventStatistic.objects.create(event=event, value="48", label="New Converts", order=3)

# Create Event Partners
EventPartner.objects.create(event=event, name="Optimizing People (Lead Organization)", order=1)
EventPartner.objects.create(event=event, name="Arise And Walk Gospel Assembly (AWGA)", order=2)
EventPartner.objects.create(event=event, name="Narrow Path Christian Church", order=3)

# Create Team Metrics
EventTeamMetric.objects.create(event=event, value="14", label="Total Volunteers", order=1)
EventTeamMetric.objects.create(event=event, value="4", label="Ministers", order=2)
EventTeamMetric.objects.create(event=event, value="1", label="Day of Service", order=3)

# Create Event Impacts
EventImpact.objects.create(
    event=event,
    title="Spiritual Impact",
    items="48 individuals surrendered their lives to Christ (Alleluyah!)\nGospel message delivered with clarity and compassion\nSpiritual counselling and prayers provided to attendees\nBibles and new convert booklets distributed",
    order=1
)

EventImpact.objects.create(
    event=event,
    title="Community Impact",
    items="Identification of 52 widows for welfare support\nSharing of food items to attendees\nDemonstration of Christ-like compassion and service",
    order=2
)

print(f"Event '{event.title}' and all related records created successfully! (ID: {event.id})")
