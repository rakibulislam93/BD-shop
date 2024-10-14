from rest_framework import serializers
from django.contrib.auth.models import User

from . import models


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class SellSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Nested serializer for GET requests
    product_id = serializers.PrimaryKeyRelatedField(source='product', queryset=models.Product.objects.all(), write_only=True)

    price_at_sell = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    class Meta:
        model = models.Sell
        # fields = ['product','product_id','quantity','price_at_sell','total_price']
        fields = '__all__'

    def create(self,validated_data):
        product = validated_data.get('product')      
        quantity = validated_data.get('quantity')
        
        price_at_sell = product.price

        total_price = price_at_sell * quantity

        sell = models.Sell.objects.create(
            product=product,
            quantity=quantity,
            price_at_sell=price_at_sell,
            total_price=total_price
        )
        return sell



class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ManageAppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ManageAppUser
        fields = '__all__'