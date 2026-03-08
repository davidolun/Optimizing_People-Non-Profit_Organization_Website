from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard Home
    path('', views.DashboardHomeView.as_view(), name='dashboard_home'),
    
    # Event CRUD
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    
    # Event Gallery CRUD
    path('events/<int:event_id>/gallery/', views.EventGalleryListView.as_view(), name='event_gallery'),
    path('events/<int:event_id>/gallery/add/', views.GalleryImageCreateView.as_view(), name='gallery_image_add'),
    path('gallery/<int:pk>/delete/', views.GalleryImageDeleteView.as_view(), name='gallery_image_delete'),

    # Event Data Cards (Statistics, Partners, Team Metrics, Impacts)
    path('events/<int:event_id>/data/', views.EventDataManageView.as_view(), name='event_data_manage'),

    # Statistics
    path('events/<int:event_id>/data/stat/add/', views.EventStatisticCreateView.as_view(), name='event_stat_add'),
    path('data/stat/<int:pk>/edit/', views.EventStatisticUpdateView.as_view(), name='event_stat_edit'),
    path('data/stat/<int:pk>/delete/', views.EventStatisticDeleteView.as_view(), name='event_stat_delete'),

    # Partners
    path('events/<int:event_id>/data/partner/add/', views.EventPartnerCreateView.as_view(), name='event_partner_add'),
    path('data/partner/<int:pk>/edit/', views.EventPartnerUpdateView.as_view(), name='event_partner_edit'),
    path('data/partner/<int:pk>/delete/', views.EventPartnerDeleteView.as_view(), name='event_partner_delete'),

    # Team Metrics
    path('events/<int:event_id>/data/metric/add/', views.EventTeamMetricCreateView.as_view(), name='event_metric_add'),
    path('data/metric/<int:pk>/edit/', views.EventTeamMetricUpdateView.as_view(), name='event_metric_edit'),
    path('data/metric/<int:pk>/delete/', views.EventTeamMetricDeleteView.as_view(), name='event_metric_delete'),

    # Impacts
    path('events/<int:event_id>/data/impact/add/', views.EventImpactCreateView.as_view(), name='event_impact_add'),
    path('data/impact/<int:pk>/edit/', views.EventImpactUpdateView.as_view(), name='event_impact_edit'),
    path('data/impact/<int:pk>/delete/', views.EventImpactDeleteView.as_view(), name='event_impact_delete'),

    # Contact Messages
    path('messages/', views.ContactMessageListView.as_view(), name='contact_message_list'),
    path('messages/<int:pk>/', views.ContactMessageDetailView.as_view(), name='contact_message_detail'),
    path('messages/<int:pk>/delete/', views.ContactMessageDeleteView.as_view(), name='contact_message_delete'),
]
