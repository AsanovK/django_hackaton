from django.shortcuts import render
from .models import Order
from rest_framework import viewsets
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permissions_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request}