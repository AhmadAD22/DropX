from django.db import models
import os
from django.conf import settings
# Create your models here.
class CommonQuestion(models.Model):
    question=models.CharField(max_length=255)
    answer=models.TextField()
    
    
class Advertisement(models.Model):
    image=models.ImageField(upload_to='media/advertisement')
    active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def delete(self, *args, **kwargs):
        # Delete the avatar image from the server if it exists
        if self.image:
            # Get the path to the avatar image file
            image_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
            if os.path.exists(image_path):
                os.remove(image_path)
        # Call the parent delete method to perform the actual deletion
        super().delete(*args, **kwargs)
        
class AppConfig(models.Model):
    order_app_enabled=models.BooleanField(default=True)
    trip_app_enabled=models.BooleanField(default=True)
    about=models.TextField()
    privacy_policy=models.TextField()
    Terms=models.TextField()
    twiter=models.URLField( max_length=200)
    facebook=models.URLField( max_length=200)
    instagram=models.URLField( max_length=200)
    youtube=models.URLField( max_length=200)
    tiktok=models.URLField( max_length=200)
    whatsapp=models.URLField( max_length=200)