from django.urls import path
from Events.views import Event

urlpatterns = [
       path('events/', Event, name='Event-name'),
]
