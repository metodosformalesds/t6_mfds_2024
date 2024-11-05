from django.contrib import admin
from django.urls import path, include, re_path
from llamascoin.views import RegisterView, LoginView, Formulario, jumioValidation
from database.views import register_routers, RequestViewSet
from services.validation import ImageNameExtractorView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from services.paypal.paypal import CreateCheckout, CaptureCheckout, CreatePayPalProductView, CreatePayPalBillingPlanView
from services.Moffin.Moffin import ObtenerSat
from services.Moffin.Reporte_BdC import Reporte
from services.Score.score import ObtenerScore
from rest_framework.routers import DefaultRouter
from services.Correos.views import simple_mail 
from services.Correos.views import html 
db_routers = register_routers()

filter_router = DefaultRouter()
filter_router.register(r'filter', RequestViewSet, basename='filter')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view(), name = 'registro'),
    path('formulario/', Formulario ,name='formulario'),
    path('jumioValidation/', jumioValidation ,name='validacion'),
    # Incluyendo las rutas de los diferentes routers de database
    path('credit_history/', include(db_routers['credit_history'].urls)),
    path('moneylender/', include(db_routers['moneylender'].urls)),
    path('borrower/', include(db_routers['borrower'].urls)),
    path('loan/', include(db_routers['loan'].urls)),
    path('user/', include(db_routers['user'].urls)),
    path('transaction/', include(db_routers['transaction'].urls)),
    path('request/', include(db_routers['request'].urls)),
    path('active_loan/', include(db_routers['active_loan'].urls)),
    path('payment/', include(db_routers['payment'].urls)),

    path('filter/', include(filter_router.urls)),
    
    path('validate_ine/', ImageNameExtractorView.as_view(), name='validate_ine'),
    
    #Endopoints de PayPal
    path("paypal/create-checkout/", CreateCheckout.as_view(), name="create-checkout"),
    path("paypal/capture-checkout/", CaptureCheckout.as_view(), name="capture-checkout"),


    path('paypal/create-product/', CreatePayPalProductView.as_view(), name='paypal-create-product'),
    path('paypal/create-plan/', CreatePayPalBillingPlanView.as_view(), name='paypal-create-plan' ),
    
    # Endpoint para el swapper
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    #Endopoints de Moffin
    path('Moffin/SAT/', ObtenerSat.as_view(), name='obtener-SAT'),
    path('Moffin/Reporte/', Reporte.as_view(), name='Reporte_BdC' ),

    #Endopoints de Score
    path('Score/score/', ObtenerScore.as_view(), name='operacion_score'),
    #Endopoints de correos
    path('correos/',simple_mail, name='simple_mail'),
    path('correos/d',html, name='mail')

]

 
