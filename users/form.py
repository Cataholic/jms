from .models import User
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django import forms


class UserAddForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'email']
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Name'}),
            'username': TextInput(attrs={'placeholder': 'username'}),
            'password': PasswordInput(attrs={'placeholder': 'password'}),
            'email': EmailInput(attrs={'placeholder': 'email'})
        }


class UserUpdateForm(ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'password', 'email', 'is_superuser', 'is_active']
        widgets = {
            'username': TextInput(attrs={'placeholder': 'username'}),
            'email': EmailInput(attrs={'placeholder': 'email'})
        }
        labels = {
            'is_superuser': 'Is Admin'
        }
