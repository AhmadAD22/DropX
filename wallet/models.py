from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User
from order.models import Order ,Coupon
import random
import string

class UserWallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    holdAmount = models.DecimalField(max_digits=10, decimal_places=2 ,blank=True, null=True)

def generateRefCode():
    characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    ref_code = ''.join(random.choice(characters) for _ in range(8))
    return ref_code

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
            PAY_TO_SERVICE='PAY_TO_SERVICE'
            PAY_TO_PRODUCT='PAY_TO_PRODUCT'
            TOPUP='TOPUP'
            WITHDRAW='WITHDRAW'
            DRIVER_COSTS='DRIVER_COSTS'
            ADMIN_COMMISSION='ADMIN_COMMISSION'
            ORDER_TAX='ORDER_TAX'
    
    class PaymentType(models.TextChoices):
            WALLET='WALLET','wallet'
            E_PAYMENT='E_PAYMENT','e-payment'
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        IN_PROGRESS = 'IN_PROGRESS'
        COMPLETED = 'COMPLETED'
        CANCELLED = 'CANCELLED'
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE,blank=True, null=True ,related_name='transactionSent')
    target = models.ForeignKey('accounts.User', on_delete=models.CASCADE,blank=True, null=True ,related_name='transactionReceived')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    oldBalance = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    newBalance = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    paymentType = models.CharField(max_length=15,blank=True, null=True,choices=PaymentType.choices)
    type = models.CharField(max_length=20)
    transactionType=models.CharField(max_length=20,choices=TransactionType.choices)
    refCode = models.CharField(max_length=8,default=generateRefCode)
    status = models.CharField(max_length=20, choices=Status.choices)
    createdAt=models.DateTimeField(auto_now_add=True)

    class Meta:
         ordering=['-createdAt']
class OrderTransactions(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,blank=True, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE,blank=True, null=True)




class TopupRequest(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    orderDescription = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmed=models.BooleanField(default=False)

# class PaymentOrder(models.Model):
#     offer=models.ForeignKey(Offer, on_delete=models.CASCADE)
#     coupon=models.ForeignKey(Coupon, on_delete=models.CASCADE,null=True)
#     orderDescription = models.TextField()
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     confirmed=models.BooleanField(default=False)