import os
import cloudinary
import cloudinary.uploader
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from frontend.models import Event, TeamMember, GalleryImage, ContactMessage, EventStatistic, EventPartner, EventTeamMetric, EventImpact
from .forms import EventForm, GalleryImageUploadForm, EventStatisticForm, EventPartnerForm, EventTeamMetricForm, EventImpactForm
from django.contrib import messages
from dotenv import load_dotenv

load_dotenv()

# Optional configurations if missing in settings
if os.getenv('CLOUDINARY_CLOUD_NAME'):
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/admin/login/'
    def test_func(self):
        return self.request.user.is_staff

class DashboardHomeView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_events'] = Event.objects.count()
        context['total_team'] = TeamMember.objects.filter(is_active=True).count()
        context['total_gallery'] = GalleryImage.objects.count()
        context['unread_messages'] = ContactMessage.objects.filter(is_read=False).count()
        context['recent_events'] = Event.objects.order_by('-date')[:5]
        return context

class EventListView(StaffRequiredMixin, ListView):
    model = Event
    template_name = 'dashboard/event_list.html'
    context_object_name = 'events'
    ordering = ['-date']

class EventCreateView(StaffRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'dashboard/event_form.html'
    success_url = reverse_lazy('dashboard:event_list')

    def form_valid(self, form):
        messages.success(self.request, 'Event created successfully!')
        return super().form_valid(form)

class EventUpdateView(StaffRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'dashboard/event_form.html'
    success_url = reverse_lazy('dashboard:event_list')

    def form_valid(self, form):
        messages.success(self.request, 'Event updated successfully!')
        return super().form_valid(form)

class EventDeleteView(StaffRequiredMixin, DeleteView):
    model = Event
    template_name = 'dashboard/event_confirm_delete.html'
    success_url = reverse_lazy('dashboard:event_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Event deleted successfully!')
        return super().delete(request, *args, **kwargs)

# --- Gallery Image Management ---

class EventGalleryListView(StaffRequiredMixin, ListView):
    model = GalleryImage
    template_name = 'dashboard/gallery_list.html'
    context_object_name = 'images'
    
    def get_queryset(self):
        self.event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        return GalleryImage.objects.filter(event=self.event).order_by('-created_at')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = self.event
        return context

class GalleryImageCreateView(StaffRequiredMixin, CreateView):
    model = GalleryImage
    form_class = GalleryImageUploadForm
    template_name = 'dashboard/gallery_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        context['event'] = self.event
        return context

    def get_success_url(self):
        return reverse('dashboard:event_gallery', kwargs={'event_id': self.kwargs['event_id']})

    def form_valid(self, form):
        self.event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        gallery_image = form.save(commit=False)
        gallery_image.event = self.event
        
        uploaded_file = self.request.FILES.get('image_file')
        if uploaded_file:
            try:
                # Upload directly securely to Cloudinary to save disk space
                result = cloudinary.uploader.upload(
                    uploaded_file, 
                    folder=f"optimizing_people/gallery_uploads/{self.event.id}",
                    quality="auto",       # Smart compression (no visible quality loss)
                    fetch_format="auto",  # Serve as WebP to modern browsers
                )
                gallery_image.image_url = result.get('secure_url')
                messages.success(self.request, 'Image successfully uploaded to Cloudinary!')
            except Exception as e:
                messages.error(self.request, f"Image upload failed: {e}")
                return self.form_invalid(form)
        
        gallery_image.save()
        return redirect(self.get_success_url())

class GalleryImageDeleteView(StaffRequiredMixin, DeleteView):
    model = GalleryImage
    template_name = 'dashboard/gallery_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('dashboard:event_gallery', kwargs={'event_id': self.object.event.id})

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        # Optionally delete from cloudinary using robust API but safe to just detach for now.
        messages.success(self.request, 'Picture successfully removed from event gallery!')
        return super().delete(request, *args, **kwargs)

# --- Contact Messages Management ---

class ContactMessageListView(StaffRequiredMixin, ListView):
    model = ContactMessage
    template_name = 'dashboard/contact_message_list.html'
    context_object_name = 'contacts'
    ordering = ['-created_at']

class ContactMessageDetailView(StaffRequiredMixin, DetailView):
    model = ContactMessage
    template_name = 'dashboard/contact_message_detail.html'
    context_object_name = 'contact_message'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if not obj.is_read:
            obj.is_read = True
            obj.save()
        return obj

class ContactMessageDeleteView(StaffRequiredMixin, DeleteView):
    model = ContactMessage
    template_name = 'dashboard/contact_message_confirm_delete.html'
    success_url = reverse_lazy('dashboard:contact_message_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Message deleted successfully!')
        return super().delete(request, *args, **kwargs)


# --- Event Data (Cards) Management ---

class EventDataManageView(StaffRequiredMixin, View):
    """Master view for managing all dynamic data cards for a specific event."""
    template_name = 'dashboard/event_data_manage.html'

    def get(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        context = {
            'event': event,
            'statistics': event.statistics.all(),
            'partners': event.partners.all(),
            'team_metrics': event.team_metrics.all(),
            'impacts': event.impacts.all(),
            'stat_form': EventStatisticForm(),
            'partner_form': EventPartnerForm(),
            'metric_form': EventTeamMetricForm(),
            'impact_form': EventImpactForm(),
        }
        return render(request, self.template_name, context)


# --- EventStatistic CRUD ---
class EventStatisticCreateView(StaffRequiredMixin, CreateView):
    model = EventStatistic
    form_class = EventStatisticForm
    template_name = 'dashboard/event_data_manage.html'

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        stat = form.save(commit=False)
        stat.event = event
        stat.save()
        messages.success(self.request, 'Statistic added successfully!')
        return redirect(reverse('dashboard:event_data_manage', kwargs={'event_id': event.id}))

    def form_invalid(self, form):
        messages.error(self.request, 'Please fill in all required fields.')
        return redirect(reverse('dashboard:event_data_manage', kwargs={'event_id': self.kwargs['event_id']}))

class EventStatisticUpdateView(StaffRequiredMixin, UpdateView):
    model = EventStatistic
    form_class = EventStatisticForm
    template_name = 'dashboard/event_data_item_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event'] = self.object.event
        ctx['item_type'] = 'Statistic'
        ctx['back_url'] = reverse('dashboard:event_data_manage', kwargs={'event_id': self.object.event.id})
        return ctx

    def get_success_url(self):
        messages.success(self.request, 'Statistic updated!')
        return reverse('dashboard:event_data_manage', kwargs={'event_id': self.object.event.id})

class EventStatisticDeleteView(StaffRequiredMixin, DeleteView):
    model = EventStatistic
    template_name = 'dashboard/event_data_item_confirm_delete.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event'] = self.object.event
        ctx['item_type'] = 'Statistic'
        ctx['item_name'] = f"{self.object.value} — {self.object.label}"
        return ctx

    def get_success_url(self):
        messages.success(self.request, 'Statistic deleted.')
        return reverse('dashboard:event_data_manage', kwargs={'event_id': self.object.event.id})


# --- EventPartner CRUD ---
class EventPartnerCreateView(StaffRequiredMixin, CreateView):
    model = EventPartner
    form_class = EventPartnerForm
    template_name = 'dashboard/event_data_manage.html'

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        partner = form.save(commit=False)
        partner.event = event
        partner.save()
        messages.success(self.request, 'Partner added!')
        return redirect(reverse('dashboard:event_data_manage', kwargs={'event_id': event.id}))

    def form_invalid(self, form):
        messages.error(self.request, 'Please fill in all required fields.')
        return redirect(reverse('dashboard:event_data_manage', kwargs={'event_id': self.kwargs['event_id']}))

class EventPartnerUpdateView(StaffRequiredMixin, UpdateView):
    model = EventPartner
    form_class = EventPartnerForm
    template_name = 'dashboard/event_data_item_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event'] = self.object.event
        ctx['item_type'] = 'Partner'
        ctx['back_url'] = reverse('dashboard:event_data_manage', kwargs={'event_id': self.object.event.id})
        return ctx

    def get_success_url(self):
        messages.success(self.request, 'Partner updated!')
        return reverse('dashboard:event_data_manage', kwargs={'event_id': self.object.event.id})

class EventPartnerDeleteView(StaffRequiredMixin, DeleteView):
    model = EventPartner
    template_name = 'dashboard/event_data_item_confirm_delete.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event'] = self.object.event
        ctx['item_type'] = 'Partner'
        ctx['item_name'] = self.object.name
        return ctx

    def get_success_url(self):
        messages.success(self.request, 'Partner deleted.')
        return reverse('dashboard:event_data_manage', kwargs={'event_id': self.object.event.id})


# --- EventTeamMetric CRUD ---
class EventTeamMetricCreateView(StaffRequiredMixin, CreateView):
    model = EventTeamMetric
    form_class = EventTeamMetricForm
    template_name = 'dashboard/event_data_manage.html'

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        metric = form.save(commit=False)
        metric.event = event
        metric.save()
        messages.success(self.request, 'Team metric added!')
        return redirect(reverse('dashboard:event_data_manage', kwargs={'event_id': event.id}))

    def form_invalid(self, form):
        messages.error(self.request, 'Please fill in all required fields.')
        return redirect(reverse('dashboard:event_data_manage', kwargs={'event_id': self.kwargs['event_id']}))

class EventTeamMetricUpdateView(StaffRequiredMixin, UpdateView):
    model = EventTeamMetric
    form_class = EventTeamMetricForm
    template_name = 'dashboard/event_data_item_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event'] = self.object.event
        ctx['item_type'] = 'Team Metric'
        ctx['back_url'] = reverse('dashboard:event_data_manage', kwargs={'event_id': self.object.event.id})
        return ctx

    def get_success_url(self):
        messages.success(self.request, 'Team metric updated!')
        return reverse('dashboard:event_data_manage', kwargs={'event_id': self.object.event.id})

class EventTeamMetricDeleteView(StaffRequiredMixin, DeleteView):
    model = EventTeamMetric
    template_name = 'dashboard/event_data_item_confirm_delete.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event'] = self.object.event
        ctx['item_type'] = 'Team Metric'
        ctx['item_name'] = f"{self.object.value} — {self.object.label}"
        return ctx

    def get_success_url(self):
        messages.success(self.request, 'Team metric deleted.')
        return reverse('dashboard:event_data_manage', kwargs={'event_id': self.object.event.id})


# --- EventImpact CRUD ---
class EventImpactCreateView(StaffRequiredMixin, CreateView):
    model = EventImpact
    form_class = EventImpactForm
    template_name = 'dashboard/event_data_manage.html'

    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        impact = form.save(commit=False)
        impact.event = event
        impact.save()
        messages.success(self.request, 'Impact section added!')
        return redirect(reverse('dashboard:event_data_manage', kwargs={'event_id': event.id}))

    def form_invalid(self, form):
        messages.error(self.request, 'Please fill in all required fields.')
        return redirect(reverse('dashboard:event_data_manage', kwargs={'event_id': self.kwargs['event_id']}))

class EventImpactUpdateView(StaffRequiredMixin, UpdateView):
    model = EventImpact
    form_class = EventImpactForm
    template_name = 'dashboard/event_data_item_form.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event'] = self.object.event
        ctx['item_type'] = 'Impact'
        ctx['back_url'] = reverse('dashboard:event_data_manage', kwargs={'event_id': self.object.event.id})
        return ctx

    def get_success_url(self):
        messages.success(self.request, 'Impact section updated!')
        return reverse('dashboard:event_data_manage', kwargs={'event_id': self.object.event.id})

class EventImpactDeleteView(StaffRequiredMixin, DeleteView):
    model = EventImpact
    template_name = 'dashboard/event_data_item_confirm_delete.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event'] = self.object.event
        ctx['item_type'] = 'Impact'
        ctx['item_name'] = self.object.title
        return ctx

    def get_success_url(self):
        messages.success(self.request, 'Impact section deleted.')
        return reverse('dashboard:event_data_manage', kwargs={'event_id': self.object.event.id})

import json
from django.http import JsonResponse

class UpdateDataOrderView(StaffRequiredMixin, View):
    """AJAX view to update the display order of data cards."""
    def post(self, request):
        try:
            data = json.loads(request.body)
            model_type = data.get('model_type')
            order_list = data.get('order_list', []) # List of IDs in new order
            
            model_map = {
                'statistic': EventStatistic,
                'partner': EventPartner,
                'metric': EventTeamMetric,
                'impact': EventImpact,
            }
            
            model = model_map.get(model_type)
            if not model:
                return JsonResponse({'success': False, 'error': 'Invalid model type'})
                
            for index, item_id in enumerate(order_list):
                model.objects.filter(id=item_id).update(order=index)
                
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
