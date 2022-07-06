from distutils.command.upload import upload
from django.db import models
from apps.category.models import Category
from django.contrib.auth import get_user_model
User = get_user_model()

class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Price')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Product')
    in_stock = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1)
    store = models.CharField(max_length=50, verbose_name='Name of store',blank=True, unique=True)


    def __str__(self):
        return self.title


class ProductImage(models.Model):
    image = models.ImageField(upload_to='images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')
    
    def __str__(self):
        return self.product.title


class ProductLogo(models.Model):
    logo = models.ImageField(upload_to='images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='logo')

    def __str__(self):
        return self.product.title


