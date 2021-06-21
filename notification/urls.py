from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('', views.notification, name='notifications'),
    path('notification/<int:pk>', views.notification_details, name='notification_details'),
]
