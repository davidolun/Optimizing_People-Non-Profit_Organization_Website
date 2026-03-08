from django import forms
from frontend.models import Event, GalleryImage, EventStatistic, EventPartner, EventTeamMetric, EventImpact

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'event_type', 'date', 'end_date', 'location', 
            'image', 'registration_url', 'is_featured', 'description'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only require image on creation (no existing instance)
        if not self.instance.pk:
            self.fields['image'].required = True
            self.fields['image'].help_text = 'Required. Upload a thumbnail image for this event.'
        else:
            self.fields['image'].required = False
            self.fields['image'].help_text = 'Leave blank to keep the current image.'

class GalleryImageUploadForm(forms.ModelForm):
    image_file = forms.ImageField(required=True, label="Select Image to Upload")
    
    class Meta:
        model = GalleryImage
        fields = ['caption']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['caption'].help_text = "Optional caption for the gallery picture."

    def clean_image_file(self):
        image = self.cleaned_data.get('image_file')
        if image:
            max_size = 10 * 1024 * 1024  # 10 MB in bytes
            if image.size > max_size:
                raise forms.ValidationError(
                    f"Image file is too large ({image.size / (1024*1024):.1f} MB). "
                    f"Maximum allowed size is 10 MB."
                )
        return image

class EventStatisticForm(forms.ModelForm):
    class Meta:
        model = EventStatistic
        fields = ['value', 'label', 'order']
        widgets = {
            'value': forms.TextInput(attrs={'placeholder': "e.g. '184' or '50+'"}),
            'label': forms.TextInput(attrs={'placeholder': "e.g. 'Total Attendance'"}),
        }

class EventPartnerForm(forms.ModelForm):
    class Meta:
        model = EventPartner
        fields = ['name', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "e.g. 'Optimizing People'"}),
        }

class EventTeamMetricForm(forms.ModelForm):
    class Meta:
        model = EventTeamMetric
        fields = ['value', 'label', 'order']
        widgets = {
            'value': forms.TextInput(attrs={'placeholder': "e.g. '14'"}),
            'label': forms.TextInput(attrs={'placeholder': "e.g. 'Total Volunteers'"}),
        }

class EventImpactForm(forms.ModelForm):
    class Meta:
        model = EventImpact
        fields = ['title', 'items', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "e.g. 'Spiritual Impact'"}),
            'items': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': "Enter each achievement on a new line.\ne.g.\n94 individuals gave their lives to Christ\nBibles distributed to converts\nFood items shared with attendees"
            }),
        }
        help_texts = {
            'items': 'Enter each bullet point on a separate line.'
        }
