from .models import Message

def unread_message_count(request):
    """
    Context processor to add unread message count to all templates.
    """
    count = 0
    if request.user.is_authenticated:
        count = Message.objects.filter(receiver=request.user, is_read=False).count()
    
    return {'unread_message_count': count} 