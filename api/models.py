from django.db import models

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
    total_price = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    sell_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product.name