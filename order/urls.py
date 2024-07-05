from django.urls import path
from .views.restaurant_views import *
from .views.driver_views import *
urlpatterns = [
# Restaurany
path('restaurant/new-orders', RestaurantNewOrderListAPIView.as_view(), name='order-list'),
path('restaurant/current-orders', RestaurantCurrentOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/previous-orders', RestaurantPreviousOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/today-orders', RestaurantTodayOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/month-orders', RestaurantMonthOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/year-orders', RestaurantYearOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/statistics-orders', RestaurantStatisticsOrdersListAPIView.as_view(), name='order-list'),
#Driver
path('driver/new-orders', DriverNewOrderListAPIView.as_view(), name='driver-new-order'),
path('driver/current-orders', DriverCurrentOrdersListAPIView.as_view(), name='driver-current-order'),
path('driver/previous-orders', DriverPreviousOrdersListAPIView.as_view(), name='driver-previous-order'),
path('driver/statistics-orders', DriverStatisticsOrdersListAPIView.as_view(), name='driver-statistics-orders'),
path('driver/accept-order', DriverAcceptOrder.as_view(), name='driver-accept-order'),
path('driver/on-way-notify', OnWayNotification.as_view(), name='driver-on-way-notify'),
path('driver/delivery-confirm', DeliveryConfirm.as_view(), name='driver-'),

path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
]