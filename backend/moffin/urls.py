from django.urls import path
from .views import Muffin

urlpatterns = [
    path('Muffin/', Muffin.as_view(), name='Muffin'),
]