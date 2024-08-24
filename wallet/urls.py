from django.urls import path
from .views.e_payment.common import *
urlpatterns = [
    path('e_payment',PaymentCallbackView.as_view()),
    path('finalize',finalizePayment,name='finalize_payment'),
]