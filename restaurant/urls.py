from django.urls import path
from .views.category_views import *
from .views.product_views import *
from .views.store_views import *


urlpatterns = [
    path('', RestaurantDataAPIView.as_view(), name='restaurant-data'),
    
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateView.as_view(), name='category-retrieve-update'),
    
    
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDeleteView.as_view(), name='product-retrieve-update-delete'),
    path('products-by-category/<int:category_id>/', ProductListByCategoryView.as_view(), name='products-by-category-list'),
    
    
    
    path('accessory-products/', AccessoryProductListCreateAPIView.as_view(), name='accessory-product-list-create'),
    path('accessory-products/<int:pk>/', AccessoryProductRetrieveUpdateDestroyAPIView.as_view(), name='accessory-product-retrieve-update-destroy'),
    
    
    
    path('restaurant-openings/', RestaurantOpeningListCreateAPIView.as_view(), name='restaurant-opening-list-create'),
    path('restaurant-openings/<int:pk>/', RestaurantOpeningRetrieveUpdateDestroyAPIView.as_view(), name='restaurant-opening-retrieve-update-destroy'),
    
    path('common-questions/', CommonQuestionListCreateAPIView.as_view(), name='common-question-list-create'),
    path('common-questions/<int:pk>/', CommonQuestionRetrieveUpdateDestroyAPIView.as_view(), name='common-question-retrieve-update-destroy'),
    
    path('reviews/', RestaurantReviewsAPIView.as_view(), name='restaurant-reviews'),
    
    
    
]