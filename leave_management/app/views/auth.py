from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from ..forms import CustomLoginForm, CustomRegisterForm
from ..models import UserProfile
from django.views.decorators.csrf import csrf_exempt

def landing_page(request):
    return render(request, 'app/landing.html')

@csrf_exempt  # Use with caution, only if necessary
def register_view(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a UserProfile for the new user
            UserProfile.objects.create(user=user)
            # Specify the backend explicitly
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("home")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomRegisterForm()
    return render(request, 'app/register.html', {'form': form})

@csrf_exempt  # Use with caution, only if necessary
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    user_profile = user.profile  # Access UserProfile using the related_name
                    if user_profile.is_admin:
                        redirect_url = reverse('admin_dashboard')
                    elif user_profile.role == 'Manager':
                        redirect_url = reverse('manager_dashboard')
                    redirect_url = reverse('home')  # Default redirect
                    return redirect(redirect_url)
                except UserProfile.DoesNotExist:
                    messages.error(request, 'User profile not found. Please contact support.')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'app/login.html', {'form': form})

def home_view(request):
    return render(request, 'app/home.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')  # Redirect to the login page or another URL


def admin_dashboard_view(request):
    return render(request, 'app/admin_dashboard.html')