from django.contrib import admin
from django.urls import path, include
from database.views import CreditHistoryViewSet, MoneylenderViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

# Creación del router y registro de los endpoints con sus respectivos basenames
credit_history_router = DefaultRouter()
credit_history_router.register(r'', CreditHistoryViewSet, basename='credit_history')

moneylender_router = DefaultRouter()
moneylender_router.register(r'', MoneylenderViewSet, basename='moneylender')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Incluyendo las rutas de los diferentes routers
    path('credit_history/', include(credit_history_router.urls)),
    path('moneylender/', include(moneylender_router.urls)),
    
    # Endpoint para ver los endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
