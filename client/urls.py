from django.urls import path
from .views.restaurant_views import *
from .views.product_views import *
urlpatterns = [
 path("restaurant-details/<int:restaurant_id>/",RestaurantDatailsApiVew.as_view()),
path("restaurant-details",RestaurantDatailsApiVew2.as_view()),

    path('favorite-products/', FavoriteProductListAPIView.as_view(), name='favorite-product-list'),

]

