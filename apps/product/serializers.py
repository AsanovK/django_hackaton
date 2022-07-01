from rest_framework import serializers
from .models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'logo', )

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get("request")
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ""
        return url

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = [{'image': image.url} for image in instance.pub_images.all()]
        return rep
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = [{'logo': logo.url} for logo in instance.pub_images.all()]
        return rep


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = ProductImageSerializer(ProductImage.objects.filter(product=instance.id), many=True).data
        return rep
