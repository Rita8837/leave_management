from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Notification

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'app/notifications.html', {'notifications': notifications})
