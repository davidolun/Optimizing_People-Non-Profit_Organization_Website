from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.utils import timezone
from .models import TeamMember, Event, Quote, ContactMessage, Donation, Activity, Belief, ServiceDetail
from .forms import ContactForm, DonationForm, NewsletterForm, VolunteerForm


class HomeView(TemplateView):
    """Homepage view with mission, activities, and beliefs"""
    template_name = 'frontend/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'featured_events': Event.objects.filter(is_featured=True, date__gte=timezone.now())[:3],
            'activities': Activity.objects.filter(is_active=True)[:3],
            'beliefs': Belief.objects.filter(is_active=True)[:3],
            'featured_quotes': Quote.objects.filter(is_featured=True)[:2],
            'team_members': TeamMember.objects.filter(is_active=True)[:4],
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
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('frontend:who_we_are')
        else:
            context = self.get_context_data()
            context['contact_form'] = form
            return render(request, self.template_name, context)


class WhatWeDoView(TemplateView):
    """What We Do page with detailed service descriptions"""
    template_name = 'frontend/what_we_do.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'activities': Activity.objects.filter(is_active=True).order_by('order'),
            'beliefs': Belief.objects.filter(is_active=True).order_by('order'),
            'service_details': ServiceDetail.objects.filter(is_active=True).order_by('order'),
        })
        return context


class QuotesView(ListView):
    """Quotes page with inspirational quotes"""
    model = Quote
    template_name = 'frontend/quotes.html'
    context_object_name = 'quotes'
    paginate_by = 6
    
    def get_queryset(self):
        return Quote.objects.all().order_by('order', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_quotes'] = Quote.objects.filter(is_featured=True)[:3]
        return context


class EventsView(ListView):
    """Events page with upcoming events"""
    model = Event
    template_name = 'frontend/events.html'
    context_object_name = 'events'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Event.objects.filter(date__gte=timezone.now()).order_by('date')
        
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
        context['featured_events'] = Event.objects.filter(is_featured=True, date__gte=timezone.now())[:3]
        context['past_events'] = Event.objects.filter(date__lt=timezone.now()).order_by('-date')[:5]
        
        # Add search context
        context['query'] = self.request.GET.get('q', '')
        context['results_count'] = self.get_queryset().count()
        
        # Add all events context (for when there's a search)
        if context['query']:
            all_events_queryset = Event.objects.filter(date__gte=timezone.now()).order_by('date')
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
    """Donation page with donation form"""
    template_name = 'frontend/donate.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'donation_form': DonationForm(),
            'donation_types': Donation.DONATION_TYPES,
        })
        return context
    
    def post(self, request, *args, **kwargs):
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save()
            messages.success(request, f'Thank you for your generous donation of ${donation.amount}! Your support makes a difference.')
            return redirect('frontend:donate')
        else:
            context = self.get_context_data()
            context['donation_form'] = form
            return render(request, self.template_name, context)


class EventDetailView(DetailView):
    """Event detail page"""
    model = Event
    template_name = 'frontend/event_detail.html'
    context_object_name = 'event'
    slug_field = 'id'
    slug_url_kwarg = 'event_id'


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
        form = NewsletterForm(request.POST)
        if form.is_valid():
            # Here you could save to database or send to email service
            return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def get_quote(request):
    """AJAX endpoint to get a random quote"""
    quote = Quote.objects.all().order_by('?').first()
    if quote:
        return JsonResponse({
            'quote': quote.quote_text,
            'author': quote.author,
            'source': quote.source
        })
    return JsonResponse({'quote': 'No quotes available'})


def search_events(request):
    """Search events by title or location"""
    query = request.GET.get('q', '')
    if query:
        events = Event.objects.filter(
            title__icontains=query
        ).filter(date__gte=timezone.now()).order_by('date')
    else:
        events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    
    context = {
        'events': events,
        'query': query,
        'results_count': events.count()
    }
    return render(request, 'frontend/events.html', context)