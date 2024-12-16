from django import forms
from django.core.exceptions import ValidationError

from .models import Order
from customers.models import Customer
from robots.validation import validate_model, validate_version


class OrderForm(forms.ModelForm):

    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = Order
        fields = ('robot_serial',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            raise ValidationError(
                'Пользователь с таким email не найден, '
                'пожалуйста зарегистрируйтесь прежде чем сделать заказ'
                )
        return email

    def clean_robot_serial(self):
        data = self.cleaned_data['robot_serial']
        model, version = data.split('-')
        unvalidated_data = {
            'model': model,
            'version': version
        }
        validate_model(unvalidated_data)
        validate_version(unvalidated_data)
        return data
