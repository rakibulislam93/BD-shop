from django.contrib import admin
from . import models

# Register your models here.



class ProductModelAdmin(admin.ModelAdmin):
    model = models.Product
    list_display = ['name','price','image']


class SellModelAdmin(admin.ModelAdmin):
    model = models.Sell
    list_display = ['product','product_price','price_at_sell','quantity','total_price','sell_date']
    def product_price(self, obj):
        return obj.product.price

class ManageAppModelAdmin(admin.ModelAdmin):
    list_display = ['id','username','password']

admin.site.register(models.Product,ProductModelAdmin)
admin.site.register(models.Sell,SellModelAdmin)
admin.site.register(models.ManageAppUser,ManageAppModelAdmin)