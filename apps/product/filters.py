from .models import Product
from django_filters import rest_framework


class ProductPriceFilter(rest_framework.FilterSet):
    min_price = rest_framework.NumberFilter(field_name='price', lookup_expr='lte')
    max_price = rest_framework.NumberFilter(field_name='price', lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['min_price', 'max_price', 'category']