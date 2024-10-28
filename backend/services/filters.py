from database.models import Request
from django_filters import rest_framework as filters

#Creacion del filterSet
class requestfilter(filters.FilterSet):
    #Filtrar por cantidad minima y maxima del prestamo
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    amount = filters.NumberFilter(field_name="amount", lookup_expr='exact')
    #Filtrar por interes
    min_interest_rate = filters.NumberFilter(field_name="interest_rate", lookup_expr='gte')
    max_interest_rate = filters.NumberFilter(field_name="interest_rate", lookup_expr='lte')
    interest_rate = filters.NumberFilter(field_name="interest_rate", lookup_expr='exact')
    #Filtrar por plazos
    min_term = filters.NumberFilter(field_name="term", lookup_expr='gte')
    max_term = filters.NumberFilter(field_name="term", lookup_expr='lte')
    term = filters.NumberFilter(field_name="term", lookup_expr='exact')
    #Filtrar por numero de pagos
    min_number_of_pays = filters.NumberFilter(field_name="number_of_pays", lookup_expr='gte')
    min_number_of_pays = filters.NumberFilter(field_name="number_of_pays", lookup_expr='lte')
    number_of_pays = filters.NumberFilter(field_name="number_of_pays", lookup_expr='exact')
    #Filtrar por fecha de publicacion
    min_publication_date = filters.DateFilter(field_name="publication_date", lookup_expr='gte')
    max_publication_date = filters.DateFilter(field_name="publication_date", lookup_expr='lte')
    publication_date = filters.DateFilter(field_name="publication_date", lookup_expr='exact')
    #Filtrar por estatus del prestamo
    status = filters.CharFilter(field_name="status", lookup_expr='iexact')

class meta:
    model = Request
    fields = ['amount','interest_rate','term','number_of_pays','publication_date','status']