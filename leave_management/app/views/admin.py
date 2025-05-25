from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from ..models import LeaveRequest
from django.contrib import messages


@login_required
def admin_leave_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to access this page.")

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        try:
            leave_request = LeaveRequest.objects.get(id=request_id)
            if action == 'approve':
                leave_request.status = 'APPROVED'
                messages.success(
                    request, f"Leave request for {leave_request.user.username} approved.")
            elif action == 'reject':
                leave_request.status = 'REJECTED'
                messages.success(
                    request, f"Leave request for {leave_request.user.username} rejected.")
            leave_request.save()
        except LeaveRequest.DoesNotExist:
            messages.error(request, "Invalid leave request.")
        return redirect('admin_leave_list')

    leave_requests = LeaveRequest.objects.all().select_related(
        'user').order_by('-created_at')
    return render(request, 'app/admin_leave_list.html', {'leave_requests': leave_requests})
