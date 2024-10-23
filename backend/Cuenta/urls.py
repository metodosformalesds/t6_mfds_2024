from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la página de inicio
    path('registro/', views.registro, name='registro'),  # Ruta para la página de registro
    path('login1/', views.login, name='login')
]