from django.urls import path
from .views.auth import login_view, landing_page, register_view, home_view, logout_view, admin_dashboard_view
from .views.leave import apply_leave, my_leaves

urlpatterns = [
    path('', landing_page, name='landing'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'), 
    path('logout/', logout_view, name='logout'),  # URL for logging out
    path('home/', home_view, name='home'),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),  # URL for admin dashboard
    path('apply_leave/', apply_leave, name='apply_leave'),  # URL for applying leave
    path('my_leaves/', my_leaves, name='my_leaves'),  # URL for viewing leave requests
]
