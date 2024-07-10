from django.db import models
from accounts.models import *
from restaurant.models import *
from django.db.models import Sum
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import decimal


class Status(models.TextChoices):
    PENDING = 'PENDING','Pending'
    IN_PROGRESS = 'IN_PROGRESS','In Progress'
    COMPLETED = 'COMPLETED','Completed'
    CANCELLED = 'CANCELLED','Cancelled'
    REJECTED='REJECTED','Rejected'

class CancelRequest(models.TextChoices):
    DRIVER='DRIVER','Driver'
    CLIENT='CLIENT','Client'
    RESTAURANT='RESTAURANT','Restaurant'
    
class CanceledBy(models.TextChoices):
    DRIVER='DRIVER','Driver'
    CLIENT='CLIENT','Client'
    RESTAURANT='RESTAURANT','Restaurant'
    
class Payment(models.TextChoices):
    WALLET='WALLET','wallet'
    E_PAYMENT='E_PAYMENT','e-payment'

class Coupon(models.Model):
    code=models.CharField(max_length=10,unique=True)
    percent=models.PositiveIntegerField()
    expireAt=models.DateField(null=True)
    times=models.PositiveIntegerField()
    isActive=models.BooleanField(default=True)
    
class OrderConfig(models.Model):
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    maxRejectedNumber=models.PositiveSmallIntegerField()
    

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    driver=models.ForeignKey("accounts.Driver",null=True,blank=True,default=None,on_delete=models.CASCADE)
    restaurantLat=models.DecimalField(max_digits=9, decimal_places=6)
    restaurantLng=models.DecimalField(max_digits=9, decimal_places=6)
    restaurantAddress=models.CharField(max_length=100)
    destinationLat=models.DecimalField(max_digits=9, decimal_places=6)
    destinationLng=models.DecimalField(max_digits=9, decimal_places=6)
    destinationAddress=models.CharField(max_length=100)
    driverLat=models.DecimalField(max_digits=9, decimal_places=6,null=True,blank=True)
    driverLng=models.DecimalField(max_digits=9, decimal_places=6,null=True,blank=True)
    payment = models.CharField(max_length=15,blank=True, null=True,choices=Payment.choices)
    status = models.CharField(max_length=20, choices=Status.choices)
    orderDate = models.DateTimeField(auto_now_add=True)
    deliveryDate = models.DateTimeField(blank=True, null=True,default=None)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)
    coupon=models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
   # transactions=models.ManyToManyField('wallet.Transaction',through='wallet.OrderTransactions')
    def __str__(self) -> str:
        return '#' +str(self.pk)

    
    
    def total_price(self):
        """Calculates the total price of the order including items and accessories."""
        total_price =decimal.Decimal('0.0')

        # Calculate total price for items
        for item in self.items.all():
            total_price += item.get_total_price()

        # Calculate total price for accessories
        for item in self.items.all():
            for accessory in item.accessories.all():
                total_price += accessory.get_total_price()

        return total_price

    
    def total_products(self):
        """Calculates the total number of products ordered."""
        return self.items.aggregate(total_products=Sum('quantity'))['total_products'] or 0
    
    def tax(self):
        tax = self.total_price() * (decimal.Decimal(15) / 100) if self.tax else decimal.Decimal(0)
        return round(tax, 2)
        
    def price_with_tax(self):
        tax = self.tax()
        price = self.total_price()
        return round(tax + price,2)
    
    def price_with_tax_with_coupon(self):
        tax = self.tax()
        price = self.total_price()
        if self.coupon:
            coupon_percent = decimal.Decimal(self.coupon.percent) / 100
            price = price - (price * coupon_percent)
        return round(tax + price, 2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    note=models.TextField(null=True,blank=True)
    def get_total_price(self):
        """Returns the total price of the order item."""
        return self.quantity * self.unitPrice
    def __str__(self) -> str:
        return self.product.name + ' '+str(self.order)
    

class OrderAccessory(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='accessories')
    accessory_product = models.ForeignKey(AccessoryProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_total_price(self):
        """Returns the total price of the order item."""
        return self.quantity * self.unitPrice
    


class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    note=models.TextField(null=True,blank=True)


class CartAccessory(models.Model):
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='accessories')
    accessory_product = models.ForeignKey(AccessoryProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)