from .models import Assets
from django.forms import ModelForm
from django.forms import TextInput, PasswordInput


class AssetForm(ModelForm):
    class Meta:
        model = Assets
        fields = '__all__'
        widgets = {
            'hostname': TextInput(attrs={'placeholder': 'Hostname'}),
            'ip': TextInput(attrs={'placeholder': 'IP'}),
            'port': TextInput(attrs={'placeholder': 'Port'}),
            'username': TextInput(attrs={'placeholder': 'Username'}),
            'password': PasswordInput(attrs={'placeholder': 'Password'}),
        }


