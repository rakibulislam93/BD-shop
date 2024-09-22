from django.contrib import admin
from . import models

# Register your models here.

class ProductModelAdmin(admin.ModelAdmin):
    model = models.Product
    list_display = ['name','price','image']


class SellModelAdmin(admin.ModelAdmin):
    model = models.Sell
    list_display = ['product','product_price','quantity','total_price','sell_date']
    def product_price(self, obj):
        return obj.product.price
    
admin.site.register(models.Product,ProductModelAdmin)
admin.site.register(models.Sell,SellModelAdmin)