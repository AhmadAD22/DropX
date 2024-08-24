from django.db import models
# Create your models here.
from django.db import models
from accounts.models import User
from order.models import Order,Trip

class UserWallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    holdAmount = models.DecimalField(max_digits=10, decimal_places=2 ,blank=True, null=True)


class PaymentOrder(models.Model):
    trans_id=models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    confirmed=models.BooleanField(default=False)
    

class PaymentTrip(models.Model):
    trans_id=models.CharField(max_length=50)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    confirmed=models.BooleanField(default=False)
