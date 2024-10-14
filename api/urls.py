from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router = DefaultRouter()
router.register('products',views.ProductViewSet)
router.register('manage_appuser',views.ManageAppUserViewSet)

urlpatterns = [

    path('',include(router.urls)),
    path('products/sell',views.SellApiView.as_view()),
    path('login/',views.LoginApiView.as_view(),name='login'),
    path('logout/',views.LogoutApiView.as_view()),
    path('change_password/<int:id>/',views.ChangePassword.as_view(), name='change_password'),
    
    
]
