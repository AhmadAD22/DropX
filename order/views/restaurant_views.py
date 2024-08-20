from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Order,Status
from ..serializers.restaurant_serializer import *
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, date
from django.utils import timezone
from django.db.models import Sum




class RestaurantNewOrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        orders = Order.objects.filter(driver__isnull=False,status='PENDING',items__product__restaurant_id=request.user.id)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)

class RestaurantCurrentOrdersListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.filter(driver__isnull=False,status='IN_PROGRESS',items__product__restaurant_id=request.user.id)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)
    
    

    
class RestaurantPreviousOrdersListAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]

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

        serializer = OrderListSerializer(orders, many=True)

        # Append the total_amount_sum to the serialized data
        data = {
            'orders': serializer.data,
            'total_amount_sum': total_amount_sum
        }

        return Response(data)


class RestaurantMonthOrdersListAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
        order.status=Status.IN_PROGRESS
        return Response({"result":"Order accepted"})
    
class RestaurantRejectOrderAPIView(APIView):

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error":"Order does not found"})
        order.status=Status.REJECTED
        return Response({"result":"Order rejected"})