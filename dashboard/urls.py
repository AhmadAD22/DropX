from django.urls import path
from .views.login_view import *
from .views.main import main_dashboard
from .views.category_views import * 
from .views.accounts.client import  *

urlpatterns = [
path('login',login_view,name="dashboard-login"),
path('logout',logout_view,name="dashboard-logout"),

path('',main_dashboard,name="main_dashboard"),

#Categories
path('categories', category_list,name='category_list'),
path('category/create/', category_create, name='category_create'),
path('category/update/<int:pk>/', category_update, name='category_update'),
path('category/delete/<int:pk>/',category_delete, name='category_delete'),

#Client
path('clients/', client_list, name='client_list'),
    path('clients/create/', client_create, name='client_create'),
    path('clients/<int:pk>/update/', client_update, name='client_update'),
    path('clients/<int:pk>/delete/', client_delete, name='client_delete'),
]