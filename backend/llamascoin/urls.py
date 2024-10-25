from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from llamascoin.views import RegisterView, LoginView
from database.views import register_routers
from services.validation import ImageNameExtractorView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from services.paypal.paypal import CreatePaymentView, SendPayoutView, PayPalReturnView, PayPalCancelView
from services.Moffin.Moffin import ObtenerSat

db_routers = register_routers()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Cuenta.urls')),
    path('', include('moffin.urls')),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    
    # Incluyendo las rutas de los diferentes routers de database
    path('credit_history/', include(db_routers['credit_history'].urls)),
    path('moneylender/', include(db_routers['moneylender'].urls)),
    path('borrower/', include(db_routers['borrower'].urls)),
    path('loan/', include(db_routers['loan'].urls)),
    path('user/', include(db_routers['user'].urls)),
    path('transaction/', include(db_routers['transaction'].urls)),
    path('request/', include(db_routers['request'].urls)),
    path('active_loan/', include(db_routers['active_loan'].urls)),

    
    path('validate_ine/', ImageNameExtractorView.as_view(), name='validate_ine'),
    
    #Endopoints de PayPal
    path('paypal/create-payment/', CreatePaymentView.as_view(), name='create-payment'),
    path('paypal/payout/', SendPayoutView.as_view(), name='send-payout'),
    path('paypal/return/', PayPalReturnView.as_view(), name='paypal-return'), 
    path('paypal/cancel/', PayPalCancelView.as_view(), name='paypal-cancel'),
    
    
    # Endpoint para el swapper
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    #Endopoints de Moffin
    path('Moffin/SAT/', ObtenerSat.as_view(), name='obtener-SAT'),
]