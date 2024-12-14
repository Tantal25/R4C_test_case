from django.urls import path

from robots.views import (
    json_robot_creation,
    robot_creation_API,
    production_report
    )


urlpatterns = [
    path(
        'json_robot_creation/',
        json_robot_creation,
        name='json_robot_creation'
        ),
    path(
        'robot_creation_API/',
        robot_creation_API,
        name='robot_creation_API'
        ),
    path(
        'production_report/',
        production_report,
        name='production_report'
        )
]
