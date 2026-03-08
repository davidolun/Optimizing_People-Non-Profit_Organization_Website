from django import template
from frontend.models import ContactMessage

register = template.Library()

@register.simple_tag
def unread_contact_messages_count():
    """Returns the count of unread contact messages from the database."""
    return ContactMessage.objects.filter(is_read=False).count()
