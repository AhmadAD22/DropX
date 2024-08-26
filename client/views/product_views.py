from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import FavoriteProduct
from ..serializers.product_serializers import *
from restaurant.models import Product
from accounts.models import Client
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from order.models import OrderItem
from django.db.models import Avg, Count,Sum

class FavoriteProductListAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        favorite_products = FavoriteProduct.objects.filter(client__phone=request.user.phone).values_list('product_id', flat=True)
        products=Product.objects.filter(id__in=favorite_products)
        serializer = ClientProductListSerializer(products, many=True,context={'request': request})
        
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = FavoriteProductSerializer(data=request.data)
            try:
                product= Product.objects.get(pk=request.data['product_id'])
            except Product.DoesNotExist:
                return Response({"error":"Product does not found"},status=status.HTTP_404_NOT_FOUND)
            try:
                client= Client.objects.get(phone=request.user.phone)
            except Client.DoesNotExist:
                return Response({"error":"Product does not found"},status=status.HTTP_404_NOT_FOUND)
                
            if serializer.is_valid():
                serializer.save(client=client,product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'error': 'This product is already added to favorites for this client.'},
                            status=status.HTTP_409_CONFLICT)
    def delete(self, request):
        try:
            product= Product.objects.get(pk=request.data['product_id'])
        except Product.DoesNotExist:
            return Response({"error":"Product does not found"},status=status.HTTP_404_NOT_FOUND)
        try:
                client= Client.objects.get(phone=request.user.phone)
        except Client.DoesNotExist:
            return Response({"error":"Product does not found"},status=status.HTTP_404_NOT_FOUND)
        try:
            favorite_product = FavoriteProduct.objects.get(client=client,product=product)
        except FavoriteProduct.DoesNotExist:
            return Response({"error":"Favorate Product does not found"},status=status.HTTP_404_NOT_FOUND)
        favorite_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductDetailsAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,product_id):
        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error":"Product does not found"},status=status.HTTP_404_NOT_FOUND)
        product_serializer=ProductSerializer(product,context={'request': request})
        return Response(product_serializer.data,status=status.HTTP_200_OK)
        



class ProductSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        products = Product.objects.filter(name__icontains=query)
        serializer = ClientProductListSerializer(products, many=True,context={'request': request})
        return Response(serializer.data)

class ProductFilterAPIView(APIView):
    def get(self, request):
        minimum_price = request.query_params.get('minimum_price')
        maximum_price = request.query_params.get('maximum_price')
        rating = request.query_params.get('rating')
        category_id = request.query_params.get('category_id')

        products = Product.objects.all()
        if category_id is not None:
            products = products.filter(category__id=category_id)
            
        if minimum_price is not None and maximum_price is not None:
            products = products.filter(price__gte=minimum_price, price__lte=maximum_price)

        if rating is not None:
            products = products.annotate(avg_rating=Avg('productreview__rating')).filter(avg_rating__gte=rating)

        

        serializer = ClientProductListSerializer(products, many=True,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MostOrderedProductsAPIView(APIView):
    def get(self, request):
        most_ordered_products = OrderItem.objects.values('product_id', 'product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:10]
        product_ids = [item['product_id'] for item in most_ordered_products]
        products = Product.objects.filter(id__in=product_ids)
        serializer = ClientProductListSerializer(products, many=True,context={'request': request})
        return Response(serializer.data)