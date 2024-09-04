from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Order,Status,OrderConfig ,RejectedBy
from ..serializers.restaurant_serializer import *
from utils.permissions import ResturantSubscripted
from datetime import datetime, date
from django.utils import timezone
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from utils.notifications import NotificationsHelper,OrdersUpdates
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Q
class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        try:
            # Perform token authentication as usual
            user_auth_tuple = super().authenticate(request)
            return user_auth_tuple
        except AuthenticationFailed as e:
            if str(e) == 'Invalid token.':
                # Raise custom AuthenticationFailed exception with a custom message
                raise AuthenticationFailed({"error": "Invalid token."})
            else:
                raise


class RestaurantNewOrderListAPIView(APIView):
    permission_classes = [ResturantSubscripted]
    # authentication_classes = [CustomTokenAuthentication]
    def get(self, request):
        
        orders = Order.objects.filter(driver__isnull=False,status=Status.DRIVER_ACCEPTED,items__product__restaurant_id=request.user.id)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)

class RestaurantCurrentOrdersListAPIView(APIView):
    permission_classes = [ResturantSubscripted]
    def get(self, request):
        orders = Order.objects.filter( Q(driver__isnull=False) & Q(items__product__restaurant_id=request.user.id)&
        (Q(status=Status.IN_PROGRESS) |
             Q(status=Status.ACCEPTED)|
             Q(status=Status.DRIVER_ACCEPTED)|
             Q(status=Status.ON_WAY)|
             Q(status=Status.RESTAURANT_COMPLETED)
             )
        ) 
        serializer = OrderListSerializer(orders, many=True)

      
        return Response(serializer.data)
    
    

    
class RestaurantPreviousOrdersListAPIView(APIView):
    permission_classes = [ResturantSubscripted]
    def get(self, request):
        complatedOrders = Order.objects.filter(driver__isnull=False,status='COMPLETED',items__product__restaurant_id=request.user.id)
        complatedOrdersSerializer = OrderListSerializer(complatedOrders, many=True)
        cancelledOrders = Order.objects.filter(driver__isnull=False,status='CANCELLED',items__product__restaurant_id=request.user.id)
        cancelledOrdersSerializer = OrderListSerializer( cancelledOrders, many=True)
        rejectedOrders = Order.objects.filter(driver__isnull=False,status='REJECTED',items__product__restaurant_id=request.user.id)
        rejectedOrdersSerializer = OrderListSerializer( rejectedOrders, many=True)
        data={
            'complatedOrders':complatedOrdersSerializer.data,
            'cancelledOrders':cancelledOrdersSerializer.data,
            'rejectedOrders':rejectedOrdersSerializer.data
        }
        return Response(data)


class RestaurantStatisticsOrdersListAPIView(APIView):
    permission_classes = [ResturantSubscripted]

    def get(self, request):
        # Get the current date, month, and year
        current_date = date.today()
        current_month = timezone.now().month
        current_year = timezone.now().year

        # Retrieve orders for today
        today_orders = Order.objects.filter(
            driver__isnull=False,
            status='COMPLETED',
            items__product__restaurant_id=request.user.id,
            orderDate__date=current_date
        )

        # Retrieve orders for this month
        month_orders = Order.objects.filter(
            driver__isnull=False,
            status='COMPLETED',
            items__product__restaurant_id=request.user.id,
            orderDate__month=current_month
        )

        # Retrieve orders for this year
        year_orders = Order.objects.filter(
            driver__isnull=False,
            status='COMPLETED',
            items__product__restaurant_id=request.user.id,
            orderDate__year=current_year
        )

        # Calculate the sum of totalAmount for each time range
        today_total_amount_sum = today_orders.aggregate(Sum('totalAmount'))['totalAmount__sum']
        month_total_amount_sum = month_orders.aggregate(Sum('totalAmount'))['totalAmount__sum']
        year_total_amount_sum = year_orders.aggregate(Sum('totalAmount'))['totalAmount__sum']

        serializer = OrderListSerializer(today_orders, many=True)

        # Append the total_amount_sum to the serialized data
        data = {
            'today_orders': serializer.data,
            'today_total_amount_sum': today_total_amount_sum,
            'month_orders': OrderListSerializer(month_orders, many=True).data,
            'month_total_amount_sum': month_total_amount_sum,
            'year_orders': OrderListSerializer(year_orders, many=True).data,
            'year_total_amount_sum': year_total_amount_sum
        }

        return Response(data)

class RestaurantTodayOrdersListAPIView(APIView):
    permission_classes = [ResturantSubscripted]

    def get(self, request):
        # Get the current date
        current_date = date.today()

        # Retrieve orders for the current date
        orders = Order.objects.filter(
            driver__isnull=False,
            status='COMPLETED',
            items__product__restaurant_id=request.user.id,
            orderDate__date=current_date
        )

        # Calculate the sum of totalAmount
        total_amount_sum = orders.aggregate(Sum('totalAmount'))['totalAmount__sum']

        serializer = OrderListSerializer(orders, many=True)

        # Append the total_amount_sum to the serialized data
        data = {
            'orders': serializer.data,
            'total_amount_sum': total_amount_sum
        }

        return Response(data)


class RestaurantMonthOrdersListAPIView(APIView):
    permission_classes = [ResturantSubscripted]

    def get(self, request):
        # Get the current month
        current_month = timezone.now().month

        # Retrieve orders for the current month
        orders = Order.objects.filter(
            driver__isnull=False,
            status='COMPLETED',
            items__product__restaurant_id=request.user.id,
            orderDate__month=current_month
        )

        serializer = OrderListSerializer(orders, many=True)
        # Calculate the sum of totalAmount
        total_amount_sum = orders.aggregate(Sum('totalAmount'))['totalAmount__sum']

        serializer = OrderListSerializer(orders, many=True)

        # Append the total_amount_sum to the serialized data
        data = {
            'orders': serializer.data,
            'total_amount_sum': total_amount_sum
        }

        return Response(data)
    
    
class RestaurantYearOrdersListAPIView(APIView):
    permission_classes = [ResturantSubscripted]

    def get(self, request):
        # Get the current year
        current_year = timezone.now().year

        # Retrieve orders for the current year
        orders = Order.objects.filter(
            driver__isnull=False,
            status='COMPLETED',
            items__product__restaurant_id=request.user.id,
            orderDate__year=current_year
        )

        serializer = OrderListSerializer(orders, many=True)
        # Calculate the sum of totalAmount
        total_amount_sum = orders.aggregate(Sum('totalAmount'))['totalAmount__sum']

        serializer = OrderListSerializer(orders, many=True)

        # Append the total_amount_sum to the serialized data
        data = {
            'orders': serializer.data,
            'total_amount_sum': total_amount_sum
        }
        return Response(data)
  
class OrderDetailAPIView(APIView):

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error":"Order does not found"})
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class RestaurantAcceptOrderAPIView(APIView):

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error":"Order does not found"})
        order.status=Status.ACCEPTED
        order.save()
        NotificationsHelper.sendOrderUpdate(
            update=OrdersUpdates.RESTAURANT_ACCEPTED,
            orderId=order,
            target=order.client,
            )
        return Response({"result":"Order accepted"})
        
class RestaurantOrderٌReadyToShippingAPIView(APIView):

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error":"Order does not found"})
        order.status=Status.RESTAURANT_COMPLETED
        order.save()
        NotificationsHelper.sendOrderUpdate(
            update=OrdersUpdates.ORDER_READR_TO_SHIPPING,
            orderId=order,
            target=order.driver,
            )
        return Response({"result":"Driver notifyed"})
        
       
class RestaurantRejectOrderAPIView(APIView):

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error":"Order does not found"},status=status.HTTP_404_NOT_FOUND)
        if order.status==Status.REJECTED:
            return Response({"error":"Order already rejected"},status=status.HTTP_409_CONFLICT)
        current_date = date.today()
        order_config=OrderConfig.objects.first()
        
        rejectedOrdersCount = Order.objects.filter(driver__isnull=False,status='REJECTED',
                                              items__product__restaurant_id=request.user.id,
                                              orderDate__date=current_date,
                                              rejectedBy=RejectedBy.RESTAURANT
                                              ).count()
        
        if(rejectedOrdersCount<=order_config.maxRejectedNumber):
            order.status=Status.REJECTED
            order.rejectedBy=RejectedBy.RESTAURANT
            order.save()
            NotificationsHelper.sendOrderUpdate(
                update=OrdersUpdates.RESTAURANT_REJECTED,
                orderId=order,
                target=order.client,
                )
            
            NotificationsHelper.sendOrderUpdate(
                update=OrdersUpdates.RESTAURANT_REJECTED,
                orderId=order,
                target=order.driver,
                )
            
            return Response({"result":"Order rejected"})
        else:
            return Response({"error":"You can't reject more than "+str(order_config.maxRejectedNumber)+" orders today"},status=status.HTTP_400_BAD_REQUEST)