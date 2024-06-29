from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Order
from ..serializers.driver_serializers import *
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, date
from django.utils import timezone
from django.db.models import Sum
from django.db.models import Q
from accounts.models import *
from utils.notifications import *


class DriverNewOrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(driver__isnull=True,status='PENDING')
        serializer = DriverOrderListSerializer(orders, many=True)
        return Response(serializer.data)
    
class DriverCurrentOrdersListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(
            Q(driver=request.user) &
            (Q(status='IN_PROGRESS') | Q(status='PENDING')) 
                  )
        serializer = DriverOrderListSerializer(orders, many=True)
        return Response(serializer.data)

class DriverPreviousOrdersListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        complatedOrders = Order.objects.filter(driver=request.user,
                                               status='COMPLETED',
                                               )
        complatedOrdersSerializer = DriverOrderListSerializer(complatedOrders, many=True)
        cancelledOrders = Order.objects.filter(driver=request.user,
                                               status='CANCELLED',
                                              )
        cancelledOrdersSerializer = DriverOrderListSerializer( cancelledOrders, many=True)
        rejectedOrders = Order.objects.filter(driver=request.user,
                                              status='REJECTED',
                                              )
        rejectedOrdersSerializer = DriverOrderListSerializer( rejectedOrders, many=True)
        data={
            'complatedOrders':complatedOrdersSerializer.data,
            'cancelledOrders':cancelledOrdersSerializer.data,
            'rejectedOrders':rejectedOrdersSerializer.data
        }
        return Response(data)
    
    

class DriverStatisticsOrdersListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the current date, month, and year
        current_date = date.today()
        current_month = timezone.now().month
        current_year = timezone.now().year

        # Retrieve orders for today
        today_orders = Order.objects.filter(
            driver=request.user,
            status='COMPLETED',
            orderDate__date=current_date
        )

        # Retrieve orders for this month
        month_orders = Order.objects.filter(
            driver=request.user,
            status='COMPLETED',
            orderDate__month=current_month
        )

        # Retrieve orders for this year
        year_orders = Order.objects.filter(
            driver=request.user,
            status='COMPLETED',
            orderDate__year=current_year
        )

        # Calculate the sum of totalAmount for each time range
        today_total_amount_sum = today_orders.aggregate(Sum('totalAmount'))['totalAmount__sum']
        month_total_amount_sum = month_orders.aggregate(Sum('totalAmount'))['totalAmount__sum']
        year_total_amount_sum = year_orders.aggregate(Sum('totalAmount'))['totalAmount__sum']

        serializer = DriverOrderListSerializer(today_orders, many=True)

        # Append the total_amount_sum to the serialized data
        data = {
            'today_orders': serializer.data,
            'today_total_amount_sum': today_total_amount_sum,
            'month_orders': DriverOrderListSerializer(month_orders, many=True).data,
            'month_total_amount_sum': month_total_amount_sum,
            'year_orders': DriverOrderListSerializer(year_orders, many=True).data,
            'year_total_amount_sum': year_total_amount_sum
        }

        return Response(data)

class RestaurantTodayOrdersListAPIView(APIView):
    permission_classes = [IsAuthenticated]

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

        serializer = DriverOrderListSerializer(orders, many=True)

        # Append the total_amount_sum to the serialized data
        data = {
            'orders': serializer.data,
            'total_amount_sum': total_amount_sum
        }

        return Response(data)


class DriverAcceptOrder(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            order=Order.objects.get(pk=request.data['order_id'])
        except Order.DoesNotExist:
            return Response({'error':'Order does not found'},status=status.HTTP_404_NOT_FOUND)
        try:
            driver=Driver.objects.get(pk=request.user.pk)
        except Driver.DoesNotExist:
            return Response({'error':'It is not a driver account'},status=status.HTTP_404_NOT_FOUND)
        if order.driver is None:
            order.driver=driver
            order.save()
            return Response({'result':'Order accepted'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error':'The order was accepted by another driver'},status=status.HTTP_400_BAD_REQUEST)
        
        
class OnWayNotification(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            order=Order.objects.get(pk=request.data['order_id'])
        except Order.DoesNotExist:
            return Response({'error':'Order does not found'},status=status.HTTP_404_NOT_FOUND)
        try:
            driver=Driver.objects.get(pk=request.user.pk)
        except Driver.DoesNotExist:
            return Response({'error':'It is not a driver account'},status=status.HTTP_404_NOT_FOUND)
        
        NotificationsHelper.sendOrderUpdate(
            update=OrdersUpdates.Driver_ON_WAY,
            orderId=order,
            target=order.client,
            )
        
        return Response({'result':'I am on my way to you'},status=status.HTTP_404_NOT_FOUND)
       
        
    
    
