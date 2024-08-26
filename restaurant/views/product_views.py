from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Product
from accounts.models import *
from ..serializers.products_serializers import *
from utils.error_handle import error_handler
from utils.permissions import ResturantSubscripted

class RetaurantPermissions(APIView):
    permission_classes=[IsAuthenticated,ResturantSubscripted]

class ProductListByCategoryView(RetaurantPermissions):
    
    def get(self, request,category_id):
        try:
           category=Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error":"Category not found!!"},status=status.HTTP_404_NOT_FOUND)
        restaurant=Restaurant.objects.get(phone=request.user.phone)
        products = Product.objects.filter(restaurant=restaurant,category=category)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)



################ Product Views###################
class ProductListCreateView(RetaurantPermissions):
    
    def get(self, request):
        restaurant=Restaurant.objects.get(phone=request.user.phone)
        products = Product.objects.filter(restaurant=restaurant)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateListProductSerializer(data=request.data, context={'request': request})
       
        if serializer.is_valid():
            restaurant=Restaurant.objects.get(phone=request.user.phone)
            serializer.save(restaurant=restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDeleteView(RetaurantPermissions):
            
    permission_classes = [IsAuthenticated] 
    def get(self, request, pk):
        try:
            product=Product.objects.get(pk=pk)
            serializer = CreateListProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error":"product not found!!"},status=status.HTTP_404_NOT_FOUND)
        

    def put(self, request, pk):
        try:
            product=Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error":"product not found!!"},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            restaurant=Restaurant.objects.get(phone=request.user.phone)
            serializer.save(restaurant=restaurant)
            return Response(serializer.data)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product =Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error":"product not found!!"},status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    
    
################Accessory Product Views##################################

class AccessoryProductListCreateAPIView(RetaurantPermissions):
    def get(self, request,product_id):
        try:
            product=Product.objects.get(id=product_id)
        except:
            return Response({"error":"product not found!!"},status=status.HTTP_404_NOT_FOUND)
        accessory_products = AccessoryProduct.objects.filter(product=product)
        serializer = AccessoryProductSerializer(accessory_products, many=True)
        return Response(serializer.data)

    def post(self, request,product_id):
        try:
            product=Product.objects.get(id=product_id)
        except:
            return Response({"error":"product not found!!"},status=status.HTTP_404_NOT_FOUND)
        serializer = CreateAccessoryProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccessoryProductRetrieveUpdateDestroyAPIView(RetaurantPermissions):
    def get(self, request, pk):
        try:
            accessory_product = AccessoryProduct.objects.get(pk=pk)
        except:
            return Response({"error":"Accessory product not found!!"},status=status.HTTP_404_NOT_FOUND)
        serializer = AccessoryProductSerializer(accessory_product)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            accessory_product = AccessoryProduct.objects.get(pk=pk)
        except:
            return Response({"error":"Accessory product not found!!"},status=status.HTTP_404_NOT_FOUND)
        serializer = AccessoryProductSerializer(accessory_product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            accessory_product = AccessoryProduct.objects.get(pk=pk)
        except:
            return Response({"error":"Accessory product not found!!"},status=status.HTTP_404_NOT_FOUND)
        accessory_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
