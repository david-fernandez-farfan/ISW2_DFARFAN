# forms.py

from django import forms
from .models import InfoRequest
from django import forms
from .models import Destination

class InfoRequestForm(forms.ModelForm):
    class Meta:
        model = InfoRequest
        fields = ["name", "email", "notes", "cruise"]

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'description', 'image']