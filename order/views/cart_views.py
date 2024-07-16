from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Cart, CartItem, CartAccessory
from ..serializers.cart_serializers import CartSerializer
from accounts.models import Client
from restaurant.models import Product,AccessoryProduct
from functools import wraps
from django.db import transaction


class CartAPIView(APIView):
    def get(self, request):
        client=Client.objects.get(username=request.user.username)
        cart ,created= Cart.objects.get_or_create(client=client)
        serializer=CartSerializer(cart)
        return Response(serializer.data)
    

class AddProductToCartAPIView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        note= request.data.get('note')
        
        try:
            client = Client.objects.get(phone=request.user.phone)
            product = Product.objects.get(id=product_id)
        except (Client.DoesNotExist, Product.DoesNotExist):
            return Response(
                {'error': 'Invalid user or product.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if product.quantity <quantity:
            return Response({'error': 'The Product quantity is insufficient'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            product.quantity-=quantity
            product.save()
        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(client=client)
            item_for_check = CartItem.objects.filter(cart=cart).first()
            if item_for_check is not None:
                if item_for_check.product.restaurant != product.restaurant:
                    return Response({'error': 'Cannot add item from another restaurant.'}, status=status.HTTP_400_BAD_REQUEST)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if created and quantity > 1:
                cart_item.quantity = quantity
                cart_item.note=note
                cart_item.save()
            if not created:
                cart_item.quantity += int(quantity)
                cart_item.save()
            return Response({'result': 'Item added to cart.'}, status=status.HTTP_200_OK)
        

class AddAccessoryProductToCartAPIView(APIView):
    def post(self, request):
        accessory_product_id = request.data.get('accessory_id')
        quantity = request.data.get('quantity')
        try:
            accessory_product=AccessoryProduct.objects.get(pk=accessory_product_id)
        except AccessoryProduct.DoesNotExist:
            return Response({'error': 'Accessory Product Does not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
          cart_item=CartItem.objects.get(product__id=accessory_product.product.id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Please add product befor add accessories'}, status=status.HTTP_400_BAD_REQUEST)
        if accessory_product.quantity<quantity:
            return Response({'error': 'The Accessory Product quantity is insufficient'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            accessory_product.quantity-=quantity
            accessory_product.save()
        accessory_item, created = CartAccessory.objects.get_or_create(
                        cart_item=cart_item,
                        accessory_product=accessory_product
                    )

        if created and quantity > 1:            
            accessory_item.quantity = quantity
            accessory_item.save()
        if not created:
            accessory_item.quantity += int(quantity)
            accessory_item.save()
        return Response({'result': 'Accessory added to cart.'}, status=status.HTTP_200_OK)
                 

