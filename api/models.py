from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    image = models.ImageField(upload_to="api/images/")

    def __str__(self) -> str:
        return self.name


class Sell(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='sell')
    quantity = models.PositiveIntegerField()
    price_at_sell = models.DecimalField(max_digits=12,decimal_places=2,blank=True,null=True)
    total_price = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    sell_date = models.DateTimeField(auto_now_add=True)

    def save(self,*args, **kwargs):
        if not self.total_price:
            self.total_price = self.price_at_sell * self.quantity
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product.name
    

class ManageAppUser(models.Model):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
    