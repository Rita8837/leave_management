from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from ..models import LeaveRequest, Notification
from django.contrib import messages
from django.db.models import Count
from django.utils.timezone import now


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
                # Create notification
                Notification.objects.create(
                    user=leave_request.user,
                    message=f"Your leave request from {leave_request.start_date} to {leave_request.end_date} has been approved."
                )
            elif action == 'reject':
                leave_request.status = 'REJECTED'
                messages.success(
                    request, f"Leave request for {leave_request.user.username} rejected.")
                # Create notification
                Notification.objects.create(
                    user=leave_request.user,
                    message=f"Your leave request from {leave_request.start_date} to {leave_request.end_date} has been rejected."
                )
            leave_request.save()
        except LeaveRequest.DoesNotExist:
            messages.error(request, "Invalid leave request.")
        return redirect('admin_leave_list')

    leave_requests = LeaveRequest.objects.all().select_related(
        'user').order_by('-created_at')

    # Report data: count of leave requests by status
    report_data = LeaveRequest.objects.values('status').annotate(count=Count('id'))

    return render(request, 'app/admin_leave_list.html', {
        'leave_requests': leave_requests,
        'report_data': report_data
    })


@login_required
def admin_leave_report(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to access this page.")

    # Generate report data: counts by status and leave type
    status_counts = LeaveRequest.objects.values('status').annotate(count=Count('id'))
    type_counts = LeaveRequest.objects.values('leave_type').annotate(count=Count('id'))

    context = {
        'status_counts': status_counts,
        'type_counts': type_counts,
    }
    return render(request, 'app/admin_leave_report.html', context)
