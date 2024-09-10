from django.db import models
# Create your models here.
from django.db import models
from accounts.models import User,RestaurantSubscription,DriverOrderSubscription,DriverTripSubscription
from order.models import Order,Trip
from django.utils import timezone

class UserWallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    holdAmount = models.DecimalField(max_digits=10, decimal_places=2 ,blank=True, null=True)
    last_withdrawal=models.DateTimeField(null=True)


class PaymentOrder(models.Model):
    trans_id=models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    confirmed=models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True,null=True)
    

class PaymentTrip(models.Model):
    trans_id=models.CharField(max_length=50)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    confirmed=models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True,null=True)
    
class RestaurantSubscriptionPayment(models.Model):
     subscription=models.ForeignKey(RestaurantSubscription,on_delete=models.CASCADE,related_name="RenewSubscription")
     duration = models.CharField(max_length=8)
     price = models.DecimalField(max_digits=8, decimal_places=2)
     paid=models.BooleanField(default=False)
     date = models.DateTimeField(auto_now_add=True,null=True)
     
class DriverOrderSubscriptionPayment(models.Model):
     subscription=models.ForeignKey(DriverOrderSubscription,on_delete=models.CASCADE,related_name="RenewOrderSubscription")
     duration = models.CharField(max_length=8)
     price = models.DecimalField(max_digits=8, decimal_places=2)
     paid=models.BooleanField(default=False)
     date = models.DateTimeField(auto_now_add=True,null=True)
     
class DriverTripSubscriptionPayment(models.Model):
     subscription=models.ForeignKey(DriverTripSubscription,on_delete=models.CASCADE,related_name="RenewTripSubscription")
     duration = models.CharField(max_length=8)
     price = models.DecimalField(max_digits=8, decimal_places=2)
     paid=models.BooleanField(default=False)
     date = models.DateTimeField(auto_now_add=True,null=True)

