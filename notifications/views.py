from django.shortcuts import render
from .models import Notification
import notifications
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def notifications_view(request):
    # fetch all notifications for the user
    notifications = Notification.objects.filter(recipient=request.user)

    unread_notifications = notifications.filter(is_read=False)
    unread_notifications.update(is_read=True)

    return render(
        request,
        "notifications/notifications_list.html",
        {"notifications": notifications},
    )
