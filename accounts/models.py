from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from django.db import models
from django.core.files.storage import default_storage
from django.contrib.auth.models import BaseUserManager
import random 
from django.core.exceptions import ValidationError
from django.db.models import Q,Avg
import os
from django.conf import settings



# Create your models here.
def upload_avatar_path(instance, filename):
        return f'User/{instance.fullName}/avatar/{filename}'
    
class UserManager(BaseUserManager):
    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)

    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('The Phone Number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
class Genders(models.TextChoices):
    MALE="M",'Male'
    FEMALE='F','Female'

class User(AbstractUser):
    last_name = None
    first_name = None
    avatar=models.ImageField(upload_to=upload_avatar_path,null=True,blank=True)
    gender=models.CharField(max_length=1,choices=Genders.choices,null=True)
    idNumber=models.CharField(max_length=10,null=True,blank=True)
    birth=models.DateField(null=True,blank=True)
    username=models.CharField(max_length=255, blank=False,null=True)
    fullName = models.CharField(max_length=255, blank=False)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=10,unique=True)
    nationality=models.CharField(max_length=50,null=True)
    is_active=models.BooleanField(default=True,blank=True)
    is_staff=models.BooleanField(default=False,blank=True)
    is_superuser=models.BooleanField(default=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,blank=True,null=True)
    latitude = models.CharField(max_length=255,null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    deleted=models.BooleanField(default=False)
    enabled=models.BooleanField(default=False)

    
    USERNAME_FIELD = 'phone'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    def delete(self, *args, **kwargs):
        # Delete the avatar image from the server if it exists
        if self.avatar:
            # Get the path to the avatar image file
            image_path = os.path.join(settings.MEDIA_ROOT, str(self.avatar))
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # Call the parent delete method to perform the actual deletion
        super().delete(*args, **kwargs)
    
class Client(User):
   
    def __str__(self):
        return self.fullName
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        # Delete the avatar from the server if it exists
        if self.avatar:
            # Get the path to the avatar file
            avatar_path = self.avatar.path
            # Delete the file from the server
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
        
        # Call the parent delete method to perform the actual deletion
        super().delete(*args, **kwargs)
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Client'
        

    
class OrderServiceSubscription(models.Model):
    DURATION_CHOICES = [
    ("شهر", "شهر"),
    ("نصف سنة", "نصف سنة"),
    ("سنة", "سنة"),
    ]
    duration=models.CharField(max_length=8,choices=DURATION_CHOICES)
    price=models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self) -> str:
        return "توصيل طلبات لمدة"+ self.duration
    
    
class MembersServiceSubscription(models.Model):
    DURATION_CHOICES = [
    ("شهر", "شهر"),
    ("نصف سنة", "نصف سنة"),
    ("سنة", "سنة"),
    ]
    duration=models.CharField(max_length=8,choices=DURATION_CHOICES)
    price=models.DecimalField(max_digits=8, decimal_places=2)
    

    def __str__(self) -> str:
        return "توصيل أفرد لمدة"+ self.duration
    
class Car(models.Model):
    carType=models.CharField(max_length=50)
   


    def __str__(self):
        return self.carType


class carCategory(models.TextChoices):
    ECONOMICAL= 'إقتصادي'
    SEDAN = 'سيدان\كروس'
    BIG= 'كبيرة 6 ركاب'
    BUSINESS='أعمال'

class Driver(User):
    bankName=models.CharField(max_length=50)
    iban=models.CharField(max_length=21)
    companyName=models.CharField(max_length=50)
    car=models.ForeignKey(Car,on_delete=models.CASCADE)
    carName=models.CharField(max_length=50)
    carCategory=models.CharField(max_length=12,choices=carCategory.choices)
    carColor=models.CharField(max_length=50)
    carModel=models.CharField(max_length=50)
    carLicense=models.ImageField(upload_to='proven/')
    drivingLicense=models.ImageField(upload_to='proven/')
    carFront=models.ImageField(upload_to='cars/')
    carBack=models.ImageField(upload_to='cars/')
    memberSubscription=models.ForeignKey(MembersServiceSubscription,null=True,on_delete=models.SET_NULL, related_name='MembersServiceSubscription')
    orderSubscription=models.ForeignKey(OrderServiceSubscription,null=True,on_delete=models.SET_NULL, related_name='OrderServiceSubscription')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        # Delete associated images
        image_fields = [
            self.carLicense,
            self.drivingLicense,
            self.carFront,
            self.carBack,
        ]

        for image_field in image_fields:
            if image_field:
                image_path = os.path.join(settings.MEDIA_ROOT, str(image_field))
                if os.path.exists(image_path):
                    os.remove(image_path)

        # Call the original delete method
        super().delete(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Driver'
    
class RestaurantSubscription(models.Model):
    DURATION_CHOICES = [
    ("شهر", "شهر"),
    ("نصف سنة", "نصف سنة"),
    ("سنة", "سنة"),
    ]
    duration=models.CharField(max_length=8,choices=DURATION_CHOICES)
    price=models.DecimalField(max_digits=8, decimal_places=2)
    

    def __str__(self) -> str:
        return "إشتراك لمدة"+ self.duration
class Restaurant(User):
    bankName=models.CharField(max_length=50)
    commercialRecordNumber=models.PositiveIntegerField()
    iban=models.CharField(max_length=21)
    restaurantName=models.CharField(max_length=50)
    description=models.TextField(null=True,blank=True)
    restaurantLogo=models.ImageField(upload_to='proven/')
    commercialRecordImage=models.ImageField(upload_to='proven/')
    restaurantSubscription=models.ForeignKey( RestaurantSubscription,on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        # Delete associated images
        image_fields = [
            self.restaurantLogo,
            self.commercialRecordImage,
        ]

        for image_field in image_fields:
            if image_field:
                image_path = os.path.join(settings.MEDIA_ROOT, str(image_field))
                if os.path.exists(image_path):
                    os.remove(image_path)

        # Call the original delete method
        super().delete(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurant'


def expireDefault():
    return datetime.now() + timedelta(minutes=5)


def otpCodeDefault():
    rand=random.Random()
    code=''
    for _ in range(4):
        code+=str(rand.randint(0,9))
    return code     

class OTPRequest(models.Model):
    class Types(models.TextChoices):
        REGISTER='REGISTER'
        RESET_PHONE='RESET_PHONE'
        FORGET_PASSWORD='FORGET_PASSWORD'
        
    phone=models.CharField(max_length=15,null=True,blank=True)
    code=models.CharField(max_length=4,default=otpCodeDefault)
    expireAt=models.DateTimeField(default=expireDefault)
    createdAt=models.DateTimeField(auto_now_add=True)
    type=models.CharField(max_length=18,choices=Types.choices)
    isUsed=models.BooleanField(default=False)
    
    def __str__(self):
        return self.code
    def is_expired(self):
        current_time = datetime.now()
        print(current_time > self.expireAt)
        return current_time > self.expireAt

    def identifier(self):
        return self.phone 

    def clean(self):
        if  self.phone in ('',None):
            raise ValidationError("should provide phone")
        return super().clean()

    def save(self, **kwargs):
        self.full_clean()
        if not self.isUsed:
            pass
        return super().save(**kwargs)
    
    def checkRateLimitReached(phone=None, **kwargs):
        current_datetime = datetime.now()
        fifteen_minutes_ago = current_datetime - timedelta(minutes=15)
        return OTPRequest.objects.filter(
            Q(phone=phone)& Q(createdAt__lt=fifteen_minutes_ago)
        ).count() >= 5
        

    
class PendingClient(models.Model):
    avatar = models.ImageField(upload_to=upload_avatar_path, null=True)
    fullName = models.CharField(max_length=60)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    otp = models.OneToOneField(OTPRequest, on_delete=models.CASCADE, related_name='pendingClient')

    def __str__(self) -> str:
        return self.phone + ' ' + self.otp.code

class PendingRestaurant(models.Model):
    gender=models.CharField(max_length=1,choices=Genders.choices)
    idNumber=models.CharField(max_length=10)
    birth=models.DateField()
    fullName = models.CharField(max_length=255)
    nationality=models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10,unique=True)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    bankName=models.CharField(max_length=50)
    iban=models.CharField(max_length=21)
    restaurantName=models.CharField(max_length=50)
    restaurantLogo=models.ImageField(upload_to='proven/')
    commercialRecordNumber=models.PositiveIntegerField()
    commercialRecordImage=models.ImageField(upload_to='proven/')
    restaurantSubscription=models.ForeignKey( RestaurantSubscription,on_delete=models.CASCADE,related_name='restaurantSubscription')
    otp = models.OneToOneField(OTPRequest,null=True,blank=True, on_delete=models.CASCADE, related_name='pendingRestaurant')
    oldPhone= models.CharField(max_length=10,null=True,default=None)

    def __str__(self) -> str:
        return self.phone 

class PendingDriver(models.Model):
        DURATION_CHOICES = [
        ("M", "شهر"),
        ("6M", "نصف سنة"),
        ("Y", "سنة"),
        ]
        avatar=models.ImageField(upload_to=upload_avatar_path)
        gender=models.CharField(max_length=1,choices=Genders.choices)
        idNumber=models.CharField(max_length=10)
        birth=models.DateField()
        fullName = models.CharField(max_length=255)
        nationality=models.CharField(max_length=50)
        email = models.EmailField(unique=True)
        phone = models.CharField(max_length=10,unique=True)
        latitude = models.CharField(max_length=255)
        longitude = models.CharField(max_length=255)
        address = models.CharField(max_length=255)
        bankName=models.CharField(max_length=50)
        iban=models.CharField(max_length=21)
        companyName=models.CharField(max_length=50)
        car=models.ForeignKey(Car,on_delete=models.CASCADE)
        carName=models.CharField(max_length=50)
        carCategory=models.CharField(max_length=12,choices=carCategory.choices)
        carModel=models.CharField(max_length=50)
        carColor=models.CharField(max_length=50)
        carLicense=models.ImageField(upload_to='proven/')
        drivingLicense=models.ImageField(upload_to='proven/')
        carFront=models.ImageField(upload_to='cars/')
        carBack=models.ImageField(upload_to='cars/')
        memberSubscription=models.ForeignKey(MembersServiceSubscription,null=True,on_delete=models.SET_NULL)
        orderSubscription=models.ForeignKey(OrderServiceSubscription,null=True,on_delete=models.SET_NULL)
        otp = models.OneToOneField(OTPRequest,null=True, on_delete=models.CASCADE, related_name='pendingDriver')
        oldPhone= models.CharField(max_length=10,null=True,default=None)