from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from llamascoin.views import RegisterView, LoginView
from database.views import CreditHistoryViewSet, MoneylenderViewSet, BorrowerViewSet, LoanViewSet, UserViewSet
from services.validation import ImageNameExtractorView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

# Creación del router y registro de los endpoints con sus respectivos basenames
credit_history_router = DefaultRouter()
credit_history_router.register(r'', CreditHistoryViewSet, basename='credit_history')

moneylender_router = DefaultRouter()
moneylender_router.register(r'', MoneylenderViewSet, basename='moneylender')

#Creacion del router y registro de los endpoints de borrower y loans
Borrower_router = DefaultRouter()
Borrower_router.register(r'', BorrowerViewSet, basename='borrower')

Loan_router = DefaultRouter()
Loan_router.register(r'', LoanViewSet, basename='loan')

user_router = DefaultRouter()
user_router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Cuenta.urls')),
    
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    # Incluyendo las rutas de los diferentes routers
    path('credit_history/', include(credit_history_router.urls)),
    path('moneylender/', include(moneylender_router.urls)),
    path('borrower/', include(Borrower_router.urls)),
    path('loan/', include(Loan_router.urls)),
    path('user/', include(user_router.urls)),
    
    path('validate-ine/', ImageNameExtractorView.as_view(), name='validate-ine'),
    
    # Endpoint para ver los endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
