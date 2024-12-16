from django import forms
from django.core.exceptions import ValidationError

from .models import Customer


class CustomerForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Customer
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email
