from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from apps.product.filters import ProductPriceFilter
from apps.product.serializers import ProductSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from .models import Product
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly

from django.contrib.auth import get_user_model
User = get_user_model()

class ProductListView(generics.ListCreateAPIView):
    # permission_classes = IsAuthenticated
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filters_class = ProductPriceFilter
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        return {'request':self.request}

class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]




    
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     'publications/1/'
    #     publication = self.get_object()
    #     publication.views_count += 1
    #     publication.save()
    #     return super(ProductViewSet, self).retrieve(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in self.permission_classes]