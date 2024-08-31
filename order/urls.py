from django.urls import path
from .views.restaurant_views import *
from .views.driver_views import *
from .views.cart_views import *
from .views.client_views import *

urlpatterns = [
# Restaurany
path('restaurant/new-orders', RestaurantNewOrderListAPIView.as_view(), name='order-list'),
path('restaurant/current-orders', RestaurantCurrentOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/previous-orders', RestaurantPreviousOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/today-orders', RestaurantTodayOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/month-orders', RestaurantMonthOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/year-orders', RestaurantYearOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/statistics-orders', RestaurantStatisticsOrdersListAPIView.as_view(), name='order-list'),
path('restaurant/accept-order/<int:pk>', RestaurantAcceptOrderAPIView.as_view(), name='restaurant-accept-order'),
path('restaurant/reject-order/<int:pk>', RestaurantRejectOrderAPIView.as_view(), name='restaurant-accept-order'),

#Driver
path('driver/new-orders', DriverNewOrderListAPIView.as_view(), name='driver-new-order'),
path('driver/current-orders', DriverCurrentOrdersListAPIView.as_view(), name='driver-current-order'),
path('driver/previous-orders', DriverPreviousOrdersListAPIView.as_view(), name='driver-previous-order'),
path('driver/statistics-orders', DriverStatisticsOrdersListAPIView.as_view(), name='driver-statistics-orders'),
path('driver/accept-order', DriverAcceptOrder.as_view(), name='driver-accept-order'),
path('driver/on-way-notify', OnWayNotification.as_view(), name='driver-on-way-notify'),
path('driver/delivery-confirm', DeliveryConfirm.as_view(), name='driver-'),
path('driver/order/<int:order_id>/', DriverOrderDetailsListAPIView.as_view(), name='driver-order-details'),

#Client
path('client/current-orders', ClientCurrentOrdersListAPIView.as_view(), name='client-current-order'),
path('client/previous-orders', ClientPreviousOrdersListAPIView.as_view(), name='client-previous-order'),
path('client/order/<int:order_id>/', ClientOrderDetailsListAPIView.as_view(), name='client-order-details'),
path('client/cancel-order/<int:order_id>/', ClientCancelOrderListAPIView.as_view(), name='client-cancel-order'),
path('client/track-order/<int:order_id>/', ClientTrackOrderAPIView.as_view(), name='client-track-order'),



path('restaurant/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),

path('cart/', CartAPIView.as_view(), name='cart-list'),
path('add-product-to-cart/', AddProductToCartAPIView.as_view(), name='add-to-cart'),
path('update-product-quantity/', UpadteItemQuantityCartAPIView.as_view(), name='update-product-quantity'),
path('add-accessory-to-cart/', AddAccessoryProductToCartAPIView.as_view(), name='add-accessory-to-cart'),
path('update-accessory-quantity/', UpadteAccessoryItemQuantityCartAPIView.as_view(), name='update-accessory-quantity'),
path('delete-product-from-cart/', DeleteItemCartAPIView.as_view(), name='delete-product-from-cart'),
path('delete-accessory-from-cart/', DeleteAccessoryItemCartAPIView.as_view(), name='delete-accessory-from-cart'),


path('checkout/', CheckoutView.as_view(), name='checkout'),


path('tripcars/', TripCarAPIView.as_view(), name='tripcar-detail'),
path('trip-order/', ClientCreateTripAPIView.as_view(), name='create-trip'),
path('add-coupon-to-trip/<int:trip_id>/', AddCouponToTrip.as_view(), name='add-coupon-to-trip'),
path('client/cancell-trip/<int:trip_id>/', ClientCancellTripAPIView.as_view(), name='cancell-trip'),
path('current-trip/', ClientCurrentTripsListAPIView.as_view(), name='current-trip'),
path('previous-trip/', ClientPreviousTripsListAPIView.as_view(), name='previous-trip'),

path('trips-driver/new/', DriverNewTripListAPIView.as_view(), name='driver-new-trips-list'),
path('trips-driver/current/', DriverCurrentTripsListAPIView.as_view(), name='driver-current-trips-list'),
path('trips-driver/previous/', DriverPreviousTripsListAPIView.as_view(), name='driver-previous-trips-list'),
path('trips-driver/statistics/', DriverStatisticsTripsListAPIView.as_view(), name='driver-statistics-trips-list'),

path('trip/<int:trip_id>/', TripDetailAPIView.as_view(), name='trip-detail'),

path('driver/accept-trip', DriverAcceptTrip.as_view(), name='driver-accept-trip'),
path('driver/reject-trip', DriverRejectTrip.as_view(), name='driver-reject-trip'),
path('driver/complate-trip', DriverComlateTrip.as_view(), name='driver-reject-trip'),
] 