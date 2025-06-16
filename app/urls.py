from django.urls import path
from .views.auth import login_view, landing_page, register_view, home_view, logout_view, admin_dashboard_view, profile_view, settings_view
from .views.leave import apply_leave, my_leaves
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from .views.admin import admin_leave_list, admin_leave_report
from .views.notifications import notifications_view
from .views.static_pages import about_view, contact_view, help_view, privacy_view
from django.conf.urls.i18n import set_language

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
    path('admin_leave_list/', admin_leave_list, name='admin_leave_list'),
    path('admin_leave_report/', admin_leave_report, name='admin_leave_report'),
    path('notifications/', notifications_view, name='notifications'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('help/', help_view, name='help'),
    path('privacy/', privacy_view, name='privacy'),
    path('settings/', settings_view, name='settings'),
    path('profile/', profile_view, name='profile'),
    path('i18n/setlang/', set_language, name='set_language'),
]
