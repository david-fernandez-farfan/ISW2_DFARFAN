# forms.py

from django import forms
from .models import InfoRequest
from django import forms
from .models import Destination
from .models import Review

class InfoRequestForm(forms.ModelForm):
    class Meta:
        model = InfoRequest
        fields = ["name", "email", "notes", "cruise"]

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'description', 'image']
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        # Ajusta los campos según tu modelo Review
        fields = ['cruise', 'rating', 'comment']