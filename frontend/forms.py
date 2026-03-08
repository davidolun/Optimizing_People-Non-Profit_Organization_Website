from django import forms
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Contact form for general inquiries"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number (Optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject of your message',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message here...',
                'rows': 5,
                'required': True
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form validation
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['subject'].required = True
        self.fields['message'].required = True

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Send email notification
            try:
                send_mail(
                    f'New Contact Form Submission: {instance.subject}',
                    f'Name: {instance.name}\nEmail: {instance.email}\nPhone: {instance.phone}\n\nMessage:\n{instance.message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error but don't fail the form submission
                print(f"Email sending failed: {e}")
        return instance



class NewsletterForm(forms.Form):
    """Newsletter subscription form"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'required': True
        })
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name (Optional)'
        }),
        required=False
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Add any additional email validation here
        return email


class VolunteerForm(forms.Form):
    """Volunteer interest form"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Full Name',
            'required': True
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'required': True
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Phone Number',
            'required': True
        })
    )
    interests = forms.MultipleChoiceField(
        choices=[
            ('medical', 'Medical/Mental Health Care'),
            ('water', 'Water Supply Projects'),
            ('food', 'Food Distribution'),
            ('admin', 'Administrative Support'),
            ('events', 'Event Planning'),
            ('other', 'Other'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=True
    )
    availability = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Tell us about your availability and any relevant experience...',
            'rows': 4,
            'required': True
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Any additional information you\'d like to share...',
            'rows': 3
        }),
        required=False
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name
