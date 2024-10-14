from django.shortcuts import render,redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status,generics
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from rest_framework import filters
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

from . import models
from . import serializers
# Create your views here.


class LoginApiView(APIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username,password=password)

            if user:
                token,created = Token.objects.get_or_create(user=user)
                login(request,user)
                return Response({'token':token.key,'user_id':user.id})
            else:
                return Response({'error':'Invalid account'})
        return Response(serializer.errors)



class LogoutApiView(APIView):
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        
        return Response({'massage':'Account logout successfully'},status=status.HTTP_200_OK)
    



class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    

class SellApiView(APIView):
    serializer_class = serializers.SellSerializer

    def get(self,request):
        search = request.query_params.get('search',None)
        start_date = request.query_params.get('start_date',None)
        end_date = request.query_params.get('end_date',None)
        queryset = models.Sell.objects.all()
        # sell = models.Sell.objects.all()

        if search == "today":
            today = timezone.now().date()
            queryset = queryset.filter(sell_date__date=today)
        elif search == 'yesterday':
            yesterday = timezone.now().date()-timezone.timedelta(days=1)
            queryset = queryset.filter(sell_date__date=yesterday)


        if start_date and end_date :
            try:
                start_date = timezone.datetime.strptime(start_date,'%Y-%m-%d').date()
                end_date = timezone.datetime.strptime(end_date,'%Y-%m-%d').date()
                queryset = queryset.filter(sell_date__date__range=[start_date,end_date])
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.SellSerializer(queryset,many=True,context={'request':request})
        
        
        today_total_sales = self.calculate_total_sales(timezone.now().date())
        yesterday_total_sales = self.calculate_total_sales(timezone.now().date()-timezone.timedelta(days=1))

        monthly_total_sales = self.calculate_monthly_sales()

        response_data = {
             'sells':serializer.data,
            'today_total': today_total_sales,
            'yesterday_total': yesterday_total_sales,
            'monthly_total': monthly_total_sales,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def calculate_total_sales(self,date):
            total = models.Sell.objects.filter(sell_date__date=date).aggregate(total=Sum('total_price'))['total']

            return total if total else 0
        
    def calculate_monthly_sales(self):
            current_month = timezone.now().date().month
            total = models.Sell.objects.filter(sell_date__month=current_month).aggregate(total=Sum('total_price'))['total']
            return total if total else 0


    def post(self,request):
        data = request.data 
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

 
class ChangePassword(generics.GenericAPIView):
    serializer_class = serializers.PasswordChangeSerializer

    def put(self, request, id):
        old_password = request.data['old_password']
        new_password = request.data['new_password']

        obj = get_user_model().objects.get(pk=id)
        if not obj.check_password(raw_password=old_password):
            return Response({'error': 'Old Password does not match'}, status=400)
        else:
            obj.set_password(new_password)
            obj.save()
            return Response({'success': 'password changed successfully'}, status=200)
    


class ManageAppUserViewSet(viewsets.ModelViewSet):
    queryset = models.ManageAppUser.objects.all()
    serializer_class = serializers.ManageAppUserSerializer
    