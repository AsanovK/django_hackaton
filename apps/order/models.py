from tkinter import CASCADE
from django.db import models
from apps.product.models import Product
from django.contrib.auth import get_user_model
User = get_user_model()


class Order(models.Model):
    ORDER_STATUS = (
        ("IN PROCESS", "in process"),
        ("COMPLETED", "completed"),
        ("DECLINED", "declined")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    status = models.CharField(max_length=30, choices=ORDER_STATUS, default='in process')
    total_cost = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    delivery_address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=15, decimal_places=3, default=0)

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        self.total_cost = self.product.price * self.quantity
        super(OrderProduct, self).save(*args, **kwargs)