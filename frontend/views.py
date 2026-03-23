from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.utils import timezone
from .models import TeamMember, Event, ContactMessage, GalleryImage
from .forms import ContactForm, NewsletterForm, VolunteerForm


def check_rate_limit(request, action, limit=5, timeout=3600):
    """
    Check if a request exceeds the limit for a specific action within a timeout period.
    Returns True if allowed, False if limit exceeded.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        
    cache_key = f'ratelimit_{action}_{ip}'
    attempts = cache.get(cache_key, 0)
    
    if attempts >= limit:
        return False
        
    cache.set(cache_key, attempts + 1, timeout)
    return True


class HomeView(TemplateView):
    """Homepage view with mission, activities, and beliefs"""
    template_name = 'frontend/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'featured_events': Event.objects.filter(is_featured=True, is_visible=True).order_by('-date')[:3],
            'team_members': TeamMember.objects.filter(is_active=True).order_by('order'),
            'gallery_images': GalleryImage.objects.filter(event__is_visible=True).order_by('?')[:20] if Event.objects.filter(is_visible=True).exists() else GalleryImage.objects.filter(event__isnull=True).order_by('?')[:20],
        })
        return context


class WhoWeAreView(TemplateView):
    """Who We Are page with team members and contact form"""
    template_name = 'frontend/who_we_are.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'team_members': TeamMember.objects.filter(is_active=True).order_by('order'),
            'contact_form': ContactForm(),
        })
        return context
    
    def post(self, request, *args, **kwargs):
        if not check_rate_limit(request, 'whoweare_contact', limit=5, timeout=3600):
            messages.error(request, 'You have submitted too many requests. Please try again later.')
            context = self.get_context_data()
            context['contact_form'] = ContactForm(request.POST)
            return render(request, self.template_name, context)
            
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('frontend:who_we_are')
        else:
            context = self.get_context_data()
            context['contact_form'] = form
            return render(request, self.template_name, context)




class EventsView(ListView):
    """Events page with upcoming events"""
    model = Event
    template_name = 'frontend/events.html'
    context_object_name = 'events'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Event.objects.filter(is_visible=True, date__gte=timezone.now()).order_by('date')
        
        # Handle search query
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                title__icontains=query
            ) | queryset.filter(
                location__icontains=query
            ).order_by('date')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_events'] = Event.objects.filter(is_featured=True, is_visible=True, date__gte=timezone.now())[:3]
        context['past_events'] = Event.objects.filter(is_visible=True, date__lt=timezone.now()).order_by('-date')[:5]
        
        # Add search context
        context['query'] = self.request.GET.get('q', '')
        context['results_count'] = self.get_queryset().count()
        
        # Add all events context (for when there's a search)
        if context['query']:
            all_events_queryset = Event.objects.filter(is_visible=True, date__gte=timezone.now()).order_by('date')
            paginator = Paginator(all_events_queryset, 6)
            page_number = self.request.GET.get('all_page', 1)
            try:
                all_page_obj = paginator.get_page(page_number)
                context['all_events'] = all_page_obj
                context['all_events_paginated'] = paginator.num_pages > 1
                context['all_page_obj'] = all_page_obj
            except:
                context['all_events'] = all_events_queryset
                context['all_events_paginated'] = False
        else:
            context['all_events'] = context['events']
            context['all_events_paginated'] = context.get('is_paginated', False)
            context['all_page_obj'] = context.get('page_obj', None)
        
        return context


class ContactView(TemplateView):
    """Contact page with contact form and information"""
    template_name = 'frontend/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contact_form': ContactForm(),
            'volunteer_form': VolunteerForm(),
            'newsletter_form': NewsletterForm(),
        })
        return context
    
    def post(self, request, *args, **kwargs):
        form_type = request.POST.get('form_type', 'contact')
        
        if not check_rate_limit(request, f'contact_{form_type}', limit=5, timeout=3600):
            messages.error(request, 'You have submitted too many requests. Please try again later.')
            context = self.get_context_data()
            if form_type == 'contact':
                context['contact_form'] = ContactForm(request.POST)
            elif form_type == 'volunteer':
                context['volunteer_form'] = VolunteerForm(request.POST)
            elif form_type == 'newsletter':
                context['newsletter_form'] = NewsletterForm(request.POST)
            return render(request, self.template_name, context)
        
        if form_type == 'contact':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you for your message! We will get back to you soon.')
                return redirect('frontend:contact')
        elif form_type == 'volunteer':
            form = VolunteerForm(request.POST)
            if form.is_valid():
                # Here you could save volunteer information to a model or send email
                messages.success(request, 'Thank you for your interest in volunteering! We will contact you soon.')
                return redirect('frontend:contact')
        elif form_type == 'newsletter':
            form = NewsletterForm(request.POST)
            if form.is_valid():
                # Here you could save newsletter subscription
                messages.success(request, 'Thank you for subscribing to our newsletter!')
                return redirect('frontend:contact')
        
        context = self.get_context_data()
        context[f'{form_type}_form'] = form
        return render(request, self.template_name, context)


class DonateView(TemplateView):
    """Donation page"""
    template_name = 'frontend/donate.html'


class EventDetailView(DetailView):
    """Event detail page"""
    model = Event
    template_name = 'frontend/event_detail.html'
    context_object_name = 'event'
    slug_field = 'id'
    slug_url_kwarg = 'event_id'
    
    def get_queryset(self):
        # Prevent non-staff users from seeing hidden events
        if self.request.user.is_staff:
            return Event.objects.all()
        return Event.objects.filter(is_visible=True)


class TeamMemberDetailView(DetailView):
    """Team member detail page"""
    model = TeamMember
    template_name = 'frontend/team_member_detail.html'
    context_object_name = 'team_member'
    slug_field = 'id'
    slug_url_kwarg = 'member_id'


def newsletter_signup(request):
    """AJAX endpoint for newsletter signup"""
    if request.method == 'POST':
        if not check_rate_limit(request, 'newsletter_ajax', limit=5, timeout=3600):
            return JsonResponse({'success': False, 'message': 'Too many requests. Please try again later.'})
            
        form = NewsletterForm(request.POST)
        if form.is_valid():
            # Here you could save to database or send to email service
            return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})




def search_events(request):
    """Search events by title or location"""
    query = request.GET.get('q', '')
    if query:
        events = Event.objects.filter(
            is_visible=True,
            title__icontains=query,
            date__gte=timezone.now()
        ).order_by('date')
    else:
        events = Event.objects.filter(is_visible=True, date__gte=timezone.now()).order_by('date')
    
    context = {
        'events': events,
        'query': query,
        'results_count': events.count()
    }
    return render(request, 'frontend/events.html', context)


class GalleryView(TemplateView):
    """Gallery page with images categorized by event"""
    template_name = 'frontend/gallery.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Events that have at least one gallery image and are visible
        events_with_images = Event.objects.filter(is_visible=True, gallery_images__isnull=False).distinct().order_by('-date')
        events_with_images = events_with_images.prefetch_related('gallery_images')
        
        # Other images (no event associated)
        other_images = GalleryImage.objects.filter(event__isnull=True).order_by('-created_at')
        
        context['events_with_images'] = events_with_images
        context['other_images'] = other_images
        return context


class ProgramsView(TemplateView):
    """Programs page showing all events dynamically"""
    template_name = 'frontend/programs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.filter(is_visible=True).order_by('-date')
        return context