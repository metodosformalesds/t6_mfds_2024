from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
from services.validation import ImageNameExtractorView
from database.views import CreditHistoryViewSet, MoneylenderViewSet, BorrowerViewSet, LoanViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
=======
from django.urls import path, include, re_path
from . import views
#from database.views import CreditHistoryViewSet, MoneylenderViewSet, BorrowerViewSet, LoanViewSet
#from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
#from rest_framework.routers import DefaultRouter
>>>>>>> refs/remotes/origin/local

# Creación del router y registro de los endpoints con sus respectivos basenames
#credit_history_router = DefaultRouter()
#credit_history_router.register(r'', CreditHistoryViewSet, basename='credit_history')

#moneylender_router = DefaultRouter()
#moneylender_router.register(r'', MoneylenderViewSet, basename='moneylender')

#Creacion del router y registro de los endpoints de borrower y loans
#Borrower_router = DefaultRouter()
#Borrower_router.register(r'', BorrowerViewSet, basename='borrower')

<<<<<<< HEAD
Loan_router = DefaultRouter()
Loan_router.register(r'', LoanViewSet, basename='loan')
=======
#Loan_router = DefaultRouter()
#Loan_router.register(r'', LoanViewSet, basename='loan')

>>>>>>> refs/remotes/origin/local
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Cuenta.urls')),
    re_path('login', views.login),
    re_path('register', views.register),
    # Incluyendo las rutas de los diferentes routers
    #path('credit_history/', include(credit_history_router.urls)),
    #path('moneylender/', include(moneylender_router.urls)),
    #path('borrower/', include(Borrower_router.urls)),
    #path('loan/', include(Loan_router.urls)),
    
    path('validate-ine/', ImageNameExtractorView.as_view(), name='validate-ine'),
    
    # Endpoint para ver los endpoints
    #path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    #path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
