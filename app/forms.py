from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser, LeaveRequest


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={
        "placeholder": "Enter your username",
        "class": "form-control",
    }))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={
        "placeholder": "Enter your password",
        "class": "form-control",
    }))

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class CustomRegisterForm(forms.ModelForm):
    # Define company roles for the dropdown
    COMPANY_ROLES = [
        # Blank choice for optional selection
        ('', 'Select a role'),
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('HR', 'HR'),
        ('Team Lead', 'Team Lead'),
        ('Director', 'Director'),
        ('Executive', 'Executive'),
    ]

    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "class": "form-control",
        })
    )
    confirm_password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm your password",
            "class": "form-control",
        })
    )
    role = forms.ChoiceField(
        label="",
        choices=COMPANY_ROLES,
        required=True,
        widget=forms.Select(attrs={
            "class": "form-control",
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']
        widgets = {
            'username': forms.TextInput(attrs={
                "placeholder": "Enter your username",
                "class": "form-control",
            }),
            'email': forms.EmailInput(attrs={
                "placeholder": "Enter your email",
                "class": "form-control",
            }),
        }
        labels = {
            'username': '',
            'email': '',
            'role': '',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_admin = False  # Ensure is_admin is False for registered users
        if commit:
            user.save()
        return user


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'leave_type', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'leave_type': forms.Select(),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }
