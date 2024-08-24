from django.urls import path,include
from .views.e_payment.common import *
from .views.e_payment.client import *
from .views.e_payment.restaurant import *
from .views.e_payment.driver import *

clientpatterns = [
      path('order/initial-payment/<int:order_id>/', ClientPayOrderAPIView.as_view(), name='client-initial-payment'),
      path('trip/initial-payment/<int:trip_id>/', ClientPayTripAPIView.as_view(), name='client-initial-payment'),
]
restaurantpatterns = [
      path('subscriptions/restaurant/initial-payment/', RestaurantPaysubscriptionAPIView.as_view(), name='restaurant-initial-payment'),
]
driverpatterns = [
      path('subscriptions/order/initial-payment/',DriverOrderPaysubscriptionAPIView.as_view(), name='driver-initial-order-payment'),
      path('subscriptions/trip/initial-payment/',DriverTripPaysubscriptionAPIView.as_view(), name='driver-initial-trip-payment'),
]
urlpatterns = [
    path('client/',include(clientpatterns)),
    path('driver/',include(driverpatterns)),
    path('restaurant/',include(restaurantpatterns)),
    path('e_payment/callback',PaymentCallbackView.as_view()),
    path('finalize',finalizePayment,name='finalize_payment'),
]