from .models import Notification


def notification_count(request):
    if request.user.is_authenticated:
        # count only the unread ones
        count = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count()
        return {"notification_count": count}
    return {"notification_count": 0}
