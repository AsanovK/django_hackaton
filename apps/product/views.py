from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from apps.product.filters import ProductPriceFilter
from apps.product.serializers import ProductSerializer
from .models import Product
from django.contrib.auth import get_user_model
User = get_user_model()


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_class = ProductPriceFilter
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        return {'request':self.request}

    
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer