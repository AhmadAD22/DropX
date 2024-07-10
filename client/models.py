from django.db import models
from accounts.models import *
from restaurant.models import *
# Create your models here.

class FavoriteProduct(models.Model):
    client=models.ForeignKey(Client, on_delete=models.CASCADE,related_name='favoritproducts')
    product=models.ForeignKey(Product , on_delete=models.CASCADE)
    class Meta:
        unique_together = ['client', 'product']