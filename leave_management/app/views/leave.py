from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from ..models import LeaveRequest
from ..forms import LeaveRequestForm  # Assuming a form is created

@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user = request.user
            # Validate that end_date is not before start_date
            if leave_request.end_date < leave_request.start_date:
                messages.error(request, "End date cannot be before start date.")
                return render(request, 'leave/apply_leave.html', {'form': form})
            
            # Optional: Additional validation (e.g., check if user has enough leave balance)
            # This would require a leave balance model or logic, which isn't shown in your models
            try:
                leave_request.save()
                messages.success(request, "Leave request submitted successfully.")
                return redirect('my_leaves')  # Redirect to a list view or dashboard
            except Exception as e:
                messages.error(request, f"Error submitting leave request: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LeaveRequestForm(initial={'start_date': timezone.now().date()})

    return render(request, 'app/apply_leave.html', {'form': form})


@login_required
def my_leaves(request):
    # Fetch all leave requests for the current user, ordered by creation date (newest first)
    leave_requests = LeaveRequest.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'app/my_leaves.html', {
        'leave_requests': leave_requests
    })