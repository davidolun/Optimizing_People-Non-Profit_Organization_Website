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
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
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


class Quote(models.Model):
    """Model for inspirational quotes"""
    CATEGORY_CHOICES = [
        ('hope', 'Hope'),
        ('service', 'Service'),
        ('witness', 'Witness'),
        ('faith', 'Faith'),
        ('love', 'Love'),
        ('peace', 'Peace'),
        ('joy', 'Joy'),
        ('wisdom', 'Wisdom'),
    ]
    
    quote_text = models.TextField()
    author = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=200, blank=True, help_text="e.g., Bible verse, book, etc.")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='hope')
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.quote_text[:50]}..."


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


class Donation(models.Model):
    """Model for tracking donations"""
    DONATION_TYPES = [
        ('general', 'General Donation'),
        ('medical', 'Medical/Mental Health Clinic'),
        ('water', 'Rural Borehole Water Supply'),
        ('food', 'Food Distribution'),
        ('other', 'Other'),
    ]

    donor_name = models.CharField(max_length=100)
    donor_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES, default='general')
    message = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"${self.amount} from {self.donor_name}"


class Activity(models.Model):
    """Model for our activities/services"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='activity_images/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title


class Belief(models.Model):
    """Model for our beliefs"""
    belief_text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.belief_text[:50] + "..."


class ServiceDetail(models.Model):
    """Model for detailed service descriptions"""
    SERVICE_TYPES = [
        ('medical', 'Medical & Mental Health Services'),
        ('water', 'Clean Water Access'),
        ('food', 'Food Security Programs'),
        ('spiritual', 'Spiritual & Community Services'),
    ]
    
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True, help_text="Image URL for the service")
    features = models.JSONField(default=list, help_text="List of features/benefits")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Service Detail"
        verbose_name_plural = "Service Details"

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.title}"