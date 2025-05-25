from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LeaveRequest


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_admin', 'is_staff')
    search_fields = ('username', 'email', 'role')
    ordering = ('username',)
    readonly_fields = ('created_at', 'updated_at')

    # Customize fields displayed in the admin form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
         'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',
         'date_joined', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'is_admin', 'password1', 'password2'),
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset  # No need for select_related since CustomUser has no ForeignKey


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'status', 'start_date', 'end_date')
    search_fields = ('user__username', 'user__email', 'leave_type', 'status')
    list_filter = ('leave_type', 'status')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optimize queries for ForeignKey to CustomUser
        return queryset.select_related('user')
