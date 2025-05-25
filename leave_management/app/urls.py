from django.urls import path
from .views.auth import login_view, landing_page, register_view, home_view, logout_view, admin_dashboard_view
from .views.leave import apply_leave, my_leaves
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from .views.admin import admin_leave_list

admin.site.login = csrf_exempt(admin.site.login)

urlpatterns = [
    path('', landing_page, name='landing'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),  # URL for logging out
    path('home/', home_view, name='home'),
    path('admin_dashboard/', admin_dashboard_view,
         name='admin_dashboard'),  # URL for admin dashboard
    # URL for applying leave
    path('apply_leave/', apply_leave, name='apply_leave'),
    # URL for viewing leave requests
    path('my_leaves/', my_leaves, name='my_leaves'),
    path('admin_leave_list/', admin_leave_list, name='admin_leave_list')
]
