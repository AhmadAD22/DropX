from django.urls import path
from .views.login_view import *
from .views.main import main_dashboard
from .views.category_views import * 
from .views.accounts.client import  *
from .views.accounts.restaurant import *
from .views.accounts.driver import *
from .views.accounts.admin import *
from .views.subscription_requests.driver import *
from .views.subscription_requests.restaurant import *
from .views.config.order import *
from .views.config.trip import *
from .views.config.subscription import *
from .views.config.app import *
from .views.coupon import *
from .views.accounts.products import *
from .views.accounts.restaurant_financial import *
from .views.accounts.driver_financial import *
from .views.question import *
urlpatterns = [
path('login',login_view,name="dashboard-login"),
path('logout',logout_view,name="dashboard-logout"),
path('',main_dashboard,name="main_dashboard"),

#Categories
path('categories', category_list,name='category_list'),
path('category/create/', category_create, name='category_create'),
path('category/update/<int:pk>/', category_update, name='category_update'),
path('category/delete/<int:pk>/',category_delete, name='category_delete'),

# Coupon
path('coupons/', coupon_list, name='coupon_list'),
path('add_coupon/', add_coupon, name='add_coupon'),
path('coupons/<int:pk>/update/',update_coupon, name='update_coupon'),
path('coupons/<int:pk>/delete/', delete_coupon, name='delete_coupon'),
#Common Questions
path('common_question/', common_question_list, name='common_question_list'),
path('common_question/create/', common_question_create, name='common_question_create'),
path('common_question/update/<int:pk>/', common_question_update, name='common_question_update'),
path('common_question/delete/<int:pk>/',common_question_delete, name='common_question_delete'),


#Products
path('products/<int:restaurant_id>', product_list, name='product_list'),
path('products/<int:restaurant_id>/add', add_product, name='add_product'),
path('products/<int:restaurant_id>/<int:product_id>/update', update_product, name='update_product'),
path('products/<int:pk>/delete', delete_product, name='delete_product'),
#Accessory Products
path('accessory/<int:restaurant_id>/<int:product_id>/add', add_accessory_product, name='add_accessory_product'),
path('restaurant/<int:restaurant_id>/product/<int:product_id>/accessory/<int:accessory_product_id>/update/', update_accessory_product, name='update_accessory_product'),
path('accessory/<int:pk>/delete',delete_accessory_product, name='delete_accessory_product'),
#Financial
path('financial/restaurant/<int:restaurant_id>', restaurant_financial_overview, name='restaurant_financial_overview'),
path('financial/driver/<int:driver_id>', driver_financial_overview, name='driver_financial_overview'),

#Accounts
    #Client
    path('clients/', client_list, name='client_list'),
    path('clients/create/', client_create, name='client_create'),
    path('clients/<int:pk>/update/', client_update, name='client_update'),
    path('clients/<int:pk>/delete/', client_delete, name='client_delete'),
    #Restaurant
    path('restaurant/create/', create_restaurant, name='create_restaurant'),
    path('restaurant/list/', restaurant_list, name='restaurant_list'),
    path('restaurant/update/<int:pk>/', update_restaurant, name='update_restaurant'),
    path('restaurant/delete/<int:pk>/', restaurant_delete, name='restaurant_delete'),
    path('restaurant/subscription/<int:pk>/',restaurant_subscription, name='restaurant_subscription'),
    path('restaurant/subscription/disable/<int:pk>/',restaurant_order_subscription_disable, name='restaurant_order_subscription_disable'),
    path('restaurant/subscription/enable/<int:pk>/',restaurant_order_subscription_enable, name='restaurant_order_subscription_enable'),
    #Drivers
    path('driver/list/', driver_list, name='driver_list'),
    path('driver/<int:pk>/',driver_details, name='driver_details'),
    path('driver/update/<int:pk>/',driver_update, name='driver_update'),
    path('driver/<int:pk>/delete/', driver_delete, name='driver_delete'),
    path('driver/subscription/<int:pk>/',driver_subscription, name='driver_subscription'),
    path('driver/subscription/disable/<int:pk>/',driver_order_subscription_disable, name='driver_order_subscription_disable'),
    path('driver/subscription/enable/<int:pk>/',driver_order_subscription_enable, name='driver_order_subscription_enable'),
    path('driver/subscription/trip/disable/<int:pk>/',driver_trip_subscription_desable, name='driver_trip_subscription_desable'),
    path('driver/subscription/trip/enable/<int:pk>/',driver_trip_subscription_enable, name='driver_trip_subscription_enable'),
    #
    path('add-user/', add_user_with_permissions, name='add_user_with_permissions'),
    path('admin/list/', admin_list, name='admin_list'),
    path('update_admin/<int:user_id>/', update_admin, name='update_admin'),
    path('delete_admin/<int:user_id>/', delete_admin, name='delete_admin'),
    path('change_password/<int:user_id>/', change_password, name='change_password'),


#Registeration Requests
    #Drivers
    path('driver/requests/list/', driver_requests_list, name='driver_requests_list'),
    path('driver/requests/<int:pk>/',driver_requests_drtails, name='driver_requests_details'),
    path('driver/requests/<int:pk>/accept',driver_accept_request, name='driver_accept_request'),
    path('driver/requests/<int:pk>/reject',driver_reject_request, name='driver_reject_request'),
    
    #Restaurant
    path('restaurant/requests/list/', restaurant_requests_list, name='restaurant_requests_list'),
    path('restaurant/requests/<int:pk>/',restaurant_requests_details, name='restaurant_requests_details'),
    path('restaurant/requests/<int:pk>/accept',restaurant_accept_request, name='restaurant_accept_request'),
    path('restaurant/requests/<int:pk>/reject',restaurant_reject_request, name='restaurant_reject_request'),
#Config
    #order
    path('order-config/', order_config_view, name='order_config_view'),
    #App
     path('app-config/', edit_app_config, name='edit_app_config'),
    #subscription
    path('subscription-config/', subscription_config_list, name='subscription_config_list'),
    path('subscription-config/<int:pk>', update_subscription_config, name='update_subscription_config'),
    #Trip
    path('list/', trip_car_list, name='trip_car_list'),
    path('add/', add_trip_car, name='add_trip_car'),
    path('update/<int:pk>/', update_trip_car, name='update_trip_car'),
    path('delete/<int:pk>/', delete_trip_car, name='delete_trip_car'),
    
    
    
]

