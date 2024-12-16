from django.urls import path

from customers.views import create_customer


urlpatterns = [path(
    'create_customer/',
    create_customer,
    name='create_customer')
    ]
