from django.contrib import admin
from django.utils.html import format_html
from .models import (
    TeamMember, Event, Quote, ContactMessage, 
    Donation, Activity, Belief, ServiceDetail
)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'position']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'bio', 'photo')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'is_featured', 'is_upcoming', 'created_at']
    list_filter = ['is_featured', 'date', 'created_at']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_featured']
    ordering = ['-date']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'date', 'location', 'image')
        }),
        ('Registration', {
            'fields': ('registration_url',),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_featured',)
        }),
    )


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['quote_preview', 'author', 'source', 'is_featured', 'order', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['quote_text', 'author', 'source']
    list_editable = ['is_featured', 'order']
    ordering = ['order', '-created_at']
    
    def quote_preview(self, obj):
        return obj.quote_text[:50] + "..." if len(obj.quote_text) > 50 else obj.quote_text
    quote_preview.short_description = 'Quote Preview'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'amount', 'donation_type', 'is_anonymous', 'created_at']
    list_filter = ['donation_type', 'is_anonymous', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'is_anonymous')
        }),
        ('Donation Details', {
            'fields': ('amount', 'donation_type', 'message')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order']
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Belief)
class BeliefAdmin(admin.ModelAdmin):
    list_display = ['belief_preview', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['belief_text']
    list_editable = ['order', 'is_active']
    ordering = ['order']
    
    def belief_preview(self, obj):
        return obj.belief_text[:50] + "..." if len(obj.belief_text) > 50 else obj.belief_text
    belief_preview.short_description = 'Belief Preview'


@admin.register(ServiceDetail)
class ServiceDetailAdmin(admin.ModelAdmin):
    list_display = ['title', 'service_type', 'order', 'is_active', 'created_at']
    list_filter = ['service_type', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'title']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('service_type', 'title', 'description', 'image_url')
        }),
        ('Features', {
            'fields': ('features',),
            'description': 'Enter each feature on a new line or as a JSON list'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


# Customize admin site
admin.site.site_header = "Optimizing People Administration"
admin.site.site_title = "Optimizing People Admin"
admin.site.index_title = "Welcome to Optimizing People Administration"