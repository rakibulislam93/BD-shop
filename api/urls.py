from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import SellApiView,ProductViewSet

router = DefaultRouter()
router.register('products',ProductViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('products/sell',SellApiView.as_view())
]
