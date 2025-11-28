# forms.py

from django import forms
from .models import InfoRequest

class InfoRequestForm(forms.ModelForm):
    class Meta:
        model = InfoRequest
        fields = ["name", "email", "notes", "cruise"]
