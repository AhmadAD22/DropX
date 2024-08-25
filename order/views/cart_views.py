from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers.cart_serializers import *
from accounts.models import Client
from restaurant.models import Product,AccessoryProduct
from functools import wraps
from django.db import transaction
from rest_framework.permissions import IsAuthenticated


class CartAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        client=Client.objects.get(phone=request.user.phone)
        cart ,created= Cart.objects.get_or_create(client=client)
        serializer=CartSerializer(cart)
        return Response(serializer.data)
    

class AddProductToCartAPIView(APIView):
    permission_classes=[IsAuthenticated]
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
    permission_classes=[IsAuthenticated]
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
                 


from django.core.exceptions import ObjectDoesNotExist

import decimal

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            cart = Cart.objects.get(client__phone=request.user.phone)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)
        cart_serializer=CartCheckoutSerializer(cart)
        return Response(cart_serializer.data,status=status.HTTP_200_OK)

        

    def post(self, request):
        try:
            cart = Cart.objects.get(client__phone=request.user.phone)
            # Check if the cart is empty
            if cart.items.count() == 0:
                return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
            
            coupon_code = request.data.get('coupon_code')
            client_name = request.data.get('client_name')
            client_phone = request.data.get('client_phone')
            client_address = request.data.get('client_address')
            client_latitude = request.data.get('client_latitude')
            client_longitude = request.data.get('client_longitude')
            delivery_date=request.data.get('delivery_date')
            # payment_method = request.data.get('payment_method')
            if any(var is None for var in [client_name, client_phone, client_latitude, client_longitude, delivery_date]):
                return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)
            # Get the order config
            order_config = OrderConfig.objects.first()

            # Calculate the total price of the cart
            total_price = cart.total_price_with_tax()

            # Apply the coupon if provided
            if coupon_code:
                coupon = Coupon.objects.filter(code=coupon_code, isActive=True).first()
                if coupon:
                    coupon_percent = decimal.Decimal(coupon.percent) / 100
                    total_price = total_price - (total_price * coupon_percent)
                    coupon.times -= 1
                    coupon.save()

            # Calculate the tax
            # tax = total_price * (order_config.tax / 100)
            client = Client.objects.get(phone=request.user.phone)
            
            # Create the order
            order = Order.objects.create(
                client=client,
                restaurantLat=cart.items.first().product.restaurant.latitude,
                restaurantLng=cart.items.first().product.restaurant.longitude,
                restaurantAddress=cart.items.first().product.restaurant.address,
                destinationLat=client_latitude,
                destinationLng=client_longitude,
                destinationAddress=client_address,
                destinationPhone=client_phone,
                destinationName=client_name,
                deliveryDate=delivery_date,
                # payment=payment_method,
                status=Status.PENDING,
                totalAmount=total_price,
                coupon=coupon
            )

            # Create the order items
            for cart_item in cart.items.all():
                order_item = OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    unitPrice=cart_item.product.price_after_offer,
                    discount=cart_item.product.offers
                )

                # Create the order accessories
                for cart_accessory in cart_item.accessories.all():
                    OrderAccessory.objects.create(
                        order_item=order_item,
                        accessory_product=cart_accessory.accessory_product,
                        quantity=cart_accessory.quantity,
                        unitPrice=cart_accessory.accessory_product.price
                    )

            # Clear the cart items and accessories
            cart.items.all().delete()
            for cart_item in cart.items.all():
                cart_item.accessories.all().delete()

            # Serialize the order and return the response
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Client.DoesNotExist:
            return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Coupon.DoesNotExist:
            return Response({'error': 'Invalid coupon code.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
