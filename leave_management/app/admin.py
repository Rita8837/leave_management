from django.contrib import admin
from .models import UserProfile, LeaveRequest

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    search_fields = ('user__username', 'user__email', 'department', 'role')
    ordering = ('user__username',)
    readonly_fields = ('user',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user')  # Optimize queries

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'leave_type', 'user')
    search_fields = ('user__username', 'reason')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    actions = ['approve_requests', 'reject_requests']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user')  # Optimize queries

    def approve_requests(self, request, queryset):
        queryset.update(status='APPROVED')
        self.message_user(request, "Selected leave requests have been approved.")
    approve_requests.short_description = "Approve selected leave requests"

    def reject_requests(self, request, queryset):
        queryset.update(status='REJECTED')
        self.message_user(request, "Selected leave requests have been rejected.")
    reject_requests.short_description = "Reject selected leave requests"