from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    # Main pages
    path('', views.HomeView.as_view(), name='home'),
    path('who-we-are/', views.WhoWeAreView.as_view(), name='who_we_are'),
    path('what-we-do/', views.WhatWeDoView.as_view(), name='what_we_do'),
    path('quotes/', views.QuotesView.as_view(), name='quotes'),
    path('events/', views.EventsView.as_view(), name='events'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('donate/', views.DonateView.as_view(), name='donate'),
    
    # Detail pages
    path('events/<int:event_id>/', views.EventDetailView.as_view(), name='event_detail'),
    path('team/<int:member_id>/', views.TeamMemberDetailView.as_view(), name='team_member_detail'),
    
    # AJAX endpoints
    path('api/newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('api/get-quote/', views.get_quote, name='get_quote'),
    path('search-events/', views.search_events, name='search_events'),
]
