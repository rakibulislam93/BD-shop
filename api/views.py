from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone

from . import models
from . import serializers
# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class SellApiView(APIView):

    serializer_class = serializers.SellCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Save the Sell instance
            sell_instance = serializer.save()

            # Prepare the response data including total_price
            response_data = {
                'id': sell_instance.id,
                'quantity': sell_instance.quantity,
                'sell_date': sell_instance.sell_date,
                'product_name': sell_instance.product.name,
                'total_price': sell_instance.total_price,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        sells = models.Sell.objects.all()  # Fetch all Sell instances
        serializer = serializers.SellRetrievSerializer(sells, many=True)  # Serialize the data

        today_total_sales = self.calculate_total_sales(timezone.now().date())
        yesterday_total_sales = self.calculate_total_sales(timezone.now().date()-timezone.timedelta(days=1))

        monthly_total_sales = self.calculate_monthly_sales()

        response_data = {
            'sales': serializer.data,
            'today_total': today_total_sales,
            'yesterday_total': yesterday_total_sales,
            'monthly_total': monthly_total_sales,
        }

        return Response(response_data,status=status.HTTP_200_OK)

    def calculate_total_sales(self,date):
            total = models.Sell.objects.filter(sell_date__date=date).aggregate(total=Sum('total_price'))['total']

            return total if total else 0
        
    def calculate_monthly_sales(self):
            current_month = timezone.now().date().month
            total = models.Sell.objects.filter(sell_date__month=current_month).aggregate(total=Sum('total_price'))['total']
            return total if total else 0
        


        