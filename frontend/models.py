from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class TeamMember(models.Model):
    """Model for team members who run the company"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(blank=True, help_text="Brief bio about the team member")
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Order of display on the page")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.position}"


class Event(models.Model):
    """Model for upcoming events"""
    EVENT_TYPES = [
        ('crusade', 'Crusade'),
        ('medical', 'Medical Outreach'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True, help_text="Optional end date for the event")
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='other')
    registration_url = models.URLField(blank=True, help_text="Optional registration link")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.date > timezone.now()

    @property
    def formatted_date_range(self):
        if not self.end_date:
            return self.date.strftime('%B %-d, %Y')
            
        if self.date.year == self.end_date.year:
            if self.date.month == self.end_date.month:
                return f"{self.date.strftime('%B %-d')}-{self.end_date.strftime('%-d, %Y')}"
            else:
                return f"{self.date.strftime('%b %-d')} - {self.end_date.strftime('%b %-d, %Y')}"
        else:
            return f"{self.date.strftime('%b %-d, %Y')} - {self.end_date.strftime('%b %-d, %Y')}"

    @property
    def thumbnail_url(self):
        if self.image:
            return self.image.url
        first_gallery = self.gallery_images.first()
        if first_gallery:
            return first_gallery.display_url
        return "https://images.unsplash.com/photo-1593113598332-cd288d649433?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80"



class ContactMessage(models.Model):
    """Model for contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class GalleryImage(models.Model):
    """Model for gallery images related to events or general"""
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="Direct Image URL (e.g. Cloudinary)")
    caption = models.CharField(max_length=200, blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_images', help_text="Leave blank if this is a general/other image")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Image for {self.event.title if self.event else 'Other'}"

    @property
    def display_url(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return ''

class EventStatistic(models.Model):
    """Model for dynamic statistics shown on an event page (e.g. Attendance, Converts)"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='statistics')
    label = models.CharField(max_length=100, help_text="e.g. 'Total Attendance', 'New Converts'")
    value = models.CharField(max_length=50, help_text="e.g. '184', '50+', or '14'")
    order = models.PositiveIntegerField(default=0, help_text="Order in which they appear")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Event Statistic"
        verbose_name_plural = "Event Statistics"

    def __str__(self):
        return f"{self.value} - {self.label} ({self.event.title})"

class EventPartner(models.Model):
    """Model for organizations or partners involved in the event"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='partners')
    name = models.CharField(max_length=100, help_text="e.g. 'Optimizing People'")
    order = models.PositiveIntegerField(default=0, help_text="Order in which they appear")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Event Partner"
        verbose_name_plural = "Event Partners"

    def __str__(self):
        return f"{self.name} ({self.event.title})"

class EventTeamMetric(models.Model):
    """Model for team-related stats shown on an event page (e.g. Volunteers, Ministers)"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='team_metrics')
    value = models.CharField(max_length=50, help_text="e.g. '14', '4'")
    label = models.CharField(max_length=100, help_text="e.g. 'Total Volunteers', 'Ministers'")
    order = models.PositiveIntegerField(default=0, help_text="Order in which they appear")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Team Metric"
        verbose_name_plural = "Team Metrics"

    def __str__(self):
        return f"{self.value} - {self.label} ({self.event.title})"

class EventImpact(models.Model):
    """Model for impact assessment categories and their list of achievements"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='impacts')
    title = models.CharField(max_length=200, help_text="e.g. 'Spiritual Impact'")
    items = models.TextField(help_text="Enter each achievement on a new line")
    order = models.PositiveIntegerField(default=0, help_text="Order in which they appear")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Event Impact"
        verbose_name_plural = "Event Impacts"

    def __str__(self):
        return f"{self.title} ({self.event.title})"
    
    def get_items_list(self):
        # Split by newlines and remove empty lines
        return [item.strip() for item in self.items.split('\n') if item.strip()]
