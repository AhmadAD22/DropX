from rest_framework import serializers
from driver.models import DriverReview

class DriverReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model=DriverReview
        exclude=['client','driver']