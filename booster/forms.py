from django import forms
from .models import BoosterRequest

class BoosterRequestForm(forms.ModelForm):
    class Meta:
        model = BoosterRequest
        fields = ['desired_rank', 'additional_notes']
