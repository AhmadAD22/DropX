from django.urls import path
from .views.restaurant_views import *
from .views.product_views import *
from .views.deiver_views import *
urlpatterns = [
    path("restaurant-details/<int:restaurant_id>/",RestaurantDatailsApiVew.as_view()),
    path("nearest-restaurant/",NearestRestaurantsAPIView.as_view()),
    path("review-restaurant/",RestaurantReviewsAPIView.as_view()),
    path("review-driver/",DriverReviewsAPIView.as_view()),
    path('favorite-products/', FavoriteProductListAPIView.as_view(), name='favorite-product-list'),
    path('product/<int:product_id>/', ProductDetailsAPIView.as_view(), name='favorite-product-list'),
    path('products/search/', ProductSearchAPIView.as_view(), name='product-search'),
    path('products/filter/', ProductFilterAPIView.as_view(), name='product-filter'),
    path('products/most-orderd/', MostOrderedProductsAPIView.as_view(), name='product-filter'),
    
    

]

