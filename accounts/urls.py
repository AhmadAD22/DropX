from .views.client_views import *
from .views.common_views import *
from .views.deiver_views import *
from .views.restaurant_views import *
from .views.admin_views import *

from django.urls import path


urlpatterns = [
    #Client Account URLS
        #Client registration
        path('client/request_register',RegisterView.as_view()),
        path('user/phone_verify',PhoneVerifyView.as_view()),
        path('client/create-account',ClientCreateAccountAPIView.as_view(),name='Client-data-post-request'),
        #Client Login
        path('client/login', ClientAuthToken.as_view()),
        #Client profile
        path('client/info-profile',ClientDataAPIView.as_view(),name='Client-data-get-request'),
        path('clients/update/', ClientUpdateAPIView.as_view(), name='client-update'),
        path('clients/phone-reset-verify', ClientPhoneResetVerifyView.as_view(), name='client-update'),
        
        
     #Common Account URLS
        #User forget password
        path('user/forget-password-request',ForgetPasswordAPIView.as_view()), 
        path('user/forget-pssword-verify-phone',ForgetPsswordVerifyPhoneAPIView.as_view()),
        path('user/update-forgotten-password',UpdateForgottenPasswordAPIView.as_view()),
        path('user/notification',NotificationsApiview.as_view()),
        #User Update password
        path('user/password-update',UserPasswordUpdateAPIView.as_view()),
        
        #Reset Phone for Driver and Restaurant
        path('user/phone-reset-verify', ResetPhoneVerifyView.as_view(), name='client-update'),
        
        #Driver
        path('driver/subscription-config',DriverSubscriptionConfigList.as_view()),
        path('driver/login', DriverAuthToken.as_view()),
        path('driver/driver-request_register',DreiverRegisterRequestView.as_view()),
        path('driver/driver-create-account',DriverCreateAccountAPIView.as_view()),
        path('driver/info-profile', DriverProfileAPIView.as_view(), name='driver-retrieve'),
        path('driver/request-update-profile', DriverRequestUpdateAPIView.as_view(), name='driver-request-update'),
        
        
        path('admin/driver-aproval-request-update', AdminAprovalDriverUpdateRequestAPIView.as_view(), name='driver-aproval-request-update'),
        path('admin/restaurant-aproval-request-update', AdminAprovalRestaurantUpdateRequestAPIView.as_view(), name='restaurant-aproval-request-update'),
        
        path('restaurant/subscription-config',RestaurantSubscriptionConfigList.as_view()),
        path('restaurant/request_register',RestaurantRegisterRequestView.as_view()),
        path('restaurant/create-account',RestaurantCreateAccountAPIView.as_view(),name='Client-data-post-request'),
        path('restaurant/login', RestaurantAuthToken.as_view()),
        path('restaurant/info-profile', RestaurantProfileAPIView.as_view(), name='restaurant-retrieve'),
        path('restaurant/request-update-profile', PendingRestaurantRequestUpdateAPIView.as_view(), name='restaurant-request-update'),
        path('restaurant/change-status', ChangeRestaurantStatus.as_view(), name='restaurant-change-status'),
        path('restaurant/renew-subscription/', RenewSubscriptionAPIView.as_view(), name='renew_subscription'),
        
             
    

]
