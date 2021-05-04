from .models import Perm
from django.forms import ModelForm


class PermForm(ModelForm):
    class Meta:
        model = Perm
        fields = '__all__'
