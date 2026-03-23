from django.contrib import admin
from django.utils.html import format_html
from .models import (
    TeamMember, Event, ContactMessage, GalleryImage, EventStatistic,
    EventPartner, EventTeamMetric, EventImpact
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
            'fields': ('name', 'position', 'bio', 'photo', 'photo_url')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
    )


class EventStatisticInline(admin.TabularInline):
    model = EventStatistic
    extra = 1

class EventPartnerInline(admin.TabularInline):
    model = EventPartner
    extra = 1

class EventTeamMetricInline(admin.TabularInline):
    model = EventTeamMetric
    extra = 1

class EventImpactInline(admin.TabularInline):
    model = EventImpact
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'end_date', 'location', 'event_type', 'is_featured', 'is_upcoming', 'created_at']
    list_filter = ['is_featured', 'event_type', 'date', 'created_at']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_featured']
    ordering = ['-date']
    date_hierarchy = 'date'
    inlines = [EventStatisticInline, EventPartnerInline, EventTeamMetricInline, EventImpactInline]
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', ('date', 'end_date'), 'location', 'event_type', 'image')
        }),
        ('Registration', {
            'fields': ('registration_url',),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_featured',)
        }),
    )



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



@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'created_at']
    list_filter = ['event', 'created_at']
    search_fields = ['caption']
    ordering = ['-created_at']


# Customize admin site
admin.site.site_header = "Optimizing People Administration"
admin.site.site_title = "Optimizing People Admin"
admin.site.index_title = "Welcome to Optimizing People Administration"