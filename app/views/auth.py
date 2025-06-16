from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from ..forms import CustomLoginForm, CustomRegisterForm, CustomUserChangeForm
from ..models import CustomUser
from django.views.decorators.csrf import csrf_exempt


def landing_page(request):
    return render(request, 'app/landing.html')


@csrf_exempt
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='app.backends.UserSiteAuthBackend')
            messages.success(
                request, "Registration successful. You are now logged in.")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomRegisterForm()
    return render(request, 'app/register.html', {'form': form})


@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend='app.backends.UserSiteAuthBackend')
                if user.is_admin:
                    return redirect('admin_dashboard')
                elif user.role == 'Manager':
                    return redirect('manager_dashboard')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'app/login.html', {'form': form})


@csrf_exempt
def home_view(request):
    return render(request, 'app/home.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')


@csrf_exempt
def admin_dashboard_view(request):
    return render(request, 'app/admin_dashboard.html')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'app/profile.html', {'form': form})


@login_required
def settings_view(request):
    # Placeholder for settings page logic
    return render(request, 'app/settings.html')
