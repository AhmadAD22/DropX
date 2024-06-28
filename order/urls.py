from django.urls import path
from .views.restaurant_views import*
urlpatterns = [
path('restaurant/new-orders', RestaurantNewOrderListAPIView.as_view(), name='order-list'),
path('restaurant/current-orders', RestaurantCurrentOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/previous-orders', RestaurantPreviousOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/today-orders', RestaurantTodayOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/month-orders', RestaurantMonthOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/year-orders', RestaurantYearOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/statistics-orders', RestaurantStatisticsOrdersListAPIView.as_view(), name='order-list'),

path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),

]