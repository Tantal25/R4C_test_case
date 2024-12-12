from django.urls import path

from robots.views import (
    robot_creation_through_fields,
    robot_creation_through_json,
    robot_creation_without_csrf
    )


urlpatterns = [
    path('fields_robot_creation/', robot_creation_through_fields),
    path('json_robot_creation/', robot_creation_through_json),
    path('robot_creation_without_csrf/', robot_creation_without_csrf)
]
