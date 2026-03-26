from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory.quantity', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Inventory
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit_price', 'line_total']
        read_only_fields = ['unit_price', 'line_total']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        self.update_total(order)
        return order

    def update_total(self, order):
        total = sum(item.line_total for item in order.items.all())
        order.total_amount = total
        order.save()