from django.urls import path
from . import views

urlpatterns = [
    path('process-url/', views.process_url, name='process_url'),
]