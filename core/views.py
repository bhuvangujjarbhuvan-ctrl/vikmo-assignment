from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sku', 'price']

class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class DealerViewSet(ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def confirm(self, request, pk=None):
        order = self.get_object()

        if order.status != 'DRAFT':
            raise ValidationError("Only draft orders can be confirmed")

        if not order.items.exists():
            raise ValidationError("Order must have at least one item")

        for item in order.items.all():
            inventory = Inventory.objects.get(product=item.product)

            if item.quantity > inventory.quantity:
                raise ValidationError(
                    f"Insufficient stock for {item.product.name}. "
                    f"Available: {inventory.quantity}, Requested: {item.quantity}"
                )

        for item in order.items.all():
            inventory = Inventory.objects.get(product=item.product)
            inventory.quantity -= item.quantity
            inventory.save()

        order.status = 'CONFIRMED'
        order.save()

        return Response({"message": "Order confirmed"})

    @action(detail=True, methods=['post'])
    def deliver(self, request, pk=None):
        order = self.get_object()

        if order.status != 'CONFIRMED':
            raise ValidationError("Only confirmed orders can be delivered")

        order.status = 'DELIVERED'
        order.save()

        return Response({"message": "Order delivered"})