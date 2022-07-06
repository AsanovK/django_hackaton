from rest_framework import serializers
from .models import Order, OrderProduct

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity', 'total_cost')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderProductSerializer(many=True, write_only=True, required=True)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=3, default=0)
    delivery_address = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = Order
        # fields = ('items', 'total_cost', 'delivery_address', 'status')
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        items = validated_data.pop('items')
        if request.user.is_authenticated:
            validated_data['user'] = request.user
        order = Order.objects.create(**validated_data)
        total_order_cost = 0 
        for item in items:
            product = item['product']
            order_product = OrderProduct.objects.create(order=order, product=product, quantity=item['quantity'])
            total_order_cost += order_product.total_cost
            
        order.total_cost = total_order_cost
        order.save()
        return order

    def to_representation(self, instanse):
        represantation = super().to_representation(instanse)
        represantation['product'] = OrderProductSerializer(OrderProduct.objects.filter(order=instanse.id), many=True).data
        return represantation