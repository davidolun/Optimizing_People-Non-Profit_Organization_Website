from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'frontend'

urlpatterns = [
    # Main pages
    path('', views.HomeView.as_view(), name='home'),
    path('who-we-are/', views.WhoWeAreView.as_view(), name='who_we_are'),
    path('events/', views.EventsView.as_view(), name='events'),
    path('programs/', views.ProgramsView.as_view(), name='programs'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('donate/', views.DonateView.as_view(), name='donate'),
    
    # Detail pages
    path('events/<int:event_id>/', views.EventDetailView.as_view(), name='event_detail'),
    path('team/<int:member_id>/', views.TeamMemberDetailView.as_view(), name='team_member_detail'),
    
    # AJAX endpoints
    path('api/newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('search-events/', views.search_events, name='search_events'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
