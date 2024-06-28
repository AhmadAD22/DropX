from django.urls import path
from .views.restaurant_views import *
urlpatterns = [
 path("restaurant-details/<int:restaurant_id>/",RestaurantDatailsApiVew.as_view()),
path("restaurant-details",RestaurantDatailsApiVew2.as_view()),

]