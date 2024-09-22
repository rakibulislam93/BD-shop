from rest_framework import serializers

from . import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'



class SellCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sell
        exclude = ['total_price']
    
    def create(self,validated_data):
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        total_price = product.price * quantity

        sell = models.Sell.objects.create(product=product,quantity=quantity,total_price=total_price)

        return sell

class SellRetrievSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    class Meta:
        model = models.Sell
        fields = ['id','quantity','sell_date','product_name','total_price']

    def get_product_name(self,obj):
        return obj.product.name