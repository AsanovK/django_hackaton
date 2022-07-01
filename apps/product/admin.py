from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.product.models import Product, ProductImage, ProductLogo



class InlineProductImage(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image',)

class InlineProductLogo(admin.TabularInline):
    model = ProductLogo
    extra = 1
    fields = ('logo',)


class ProductAdmin(admin.ModelAdmin):
    inlines = [InlineProductImage, InlineProductLogo]
    list_display = ('title', 'in_stock', 'price', 'image', 'logo', 'store')
    list_filter = ('category', )

    def image(self, obj):
        img = obj.image.first()
        if img:
            return mark_safe(f"<img src='{img.image.url}' width='80' height='80' style='object-fit: contain' /> ")
        else:
            return ""

    def logo(self, obj):
        log = obj.logo.first()
        if log:
            return mark_safe(f"<img src='{log.logo.url}' width='80' height='80' style='object-fit: contain' /> ")
        else:
            return ""

            
admin.site.register(Product, ProductAdmin)