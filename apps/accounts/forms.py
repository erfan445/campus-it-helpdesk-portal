from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    department = forms.CharField(max_length=80, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'department']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['department', 'phone_extension', 'job_title']
