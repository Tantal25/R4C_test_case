from django import forms

from .models import Robot
from .validation import validate_model


class RobotForm(forms.ModelForm):

    class Meta:
        model = Robot
        fields = ("model", "version", "created")
        widgets = {'created': forms.DateTimeInput(
            attrs={'type': 'datetime-local'})}

    def clean(self):
        cleaned_data = super().clean()
        validate_model(cleaned_data["model"])
        return cleaned_data