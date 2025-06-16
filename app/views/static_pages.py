from django.shortcuts import render

def about_view(request):
    return render(request, 'app/about.html')

def contact_view(request):
    return render(request, 'app/contact.html')

def help_view(request):
    return render(request, 'app/help.html')

def privacy_view(request):
    return render(request, 'app/privacy.html')
