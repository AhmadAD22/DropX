from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import FavoriteProduct
from ..serializers.product_serializers import FavoriteProductSerializer
from restaurant.models import Product
from accounts.models import Client
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError


class FavoriteProductListAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        favorite_products = FavoriteProduct.objects.filter(client__phone=request.user.phone)
        serializer = FavoriteProductSerializer(favorite_products, many=True)
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


