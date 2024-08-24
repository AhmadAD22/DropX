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
from wallet.models import UserWallet,PaymentTrip
from django.db import transaction



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
    @transaction.atomic
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
        
        return Response({'result':'I am on my way to you'},status=status.HTTP_200_OK)
       
       
       
class DeliveryConfirm(APIView):
    permission_classes=[IsAuthenticated]
    @transaction.atomic
    def post(self,request):
        try:
            order=Order.objects.get(id=request.data['order_id'])
            restaurant=order.items.first().product.restaurant
            driver_wallet=UserWallet.objects.get(user__phone=order.driver.phone)
            restaurant_wallet=UserWallet.objects.get(user__phone=restaurant.phone)
        except Order.DoesNotExist:
            return Response({'error':'Order does not found'},status=status.HTTP_404_NOT_FOUND)
        except UserWallet.DoesNotExist:
            return Response({'error':'Driver or Restuaurant does not have wallet'},status=status.HTTP_404_NOT_FOUND)
        
        if order.status==Status.IN_PROGRESS:
            order.status=Status.COMPLETED
            order.save()
            total_price_for_restaurant=order.total_price()
            restaurant_wallet.balance+=Decimal(total_price_for_restaurant)
            restaurant_wallet.save()
            delivery_cost=order.deliveryCost()
            driver_wallet.balance+=Decimal(delivery_cost)
            driver_wallet.save()
            
            NotificationsHelper.sendOrderUpdate(
                update=OrdersUpdates.ORDER_COMPLETE,
                orderId=order,
                target=restaurant,
                )
            NotificationsHelper.sendOrderUpdate(
                update=OrdersUpdates.ORDER_COMPLETE,
                orderId=order,
                target=order.client,
                )
            return Response({'result':'The order delivered'},status=status.HTTP_200_OK)
        else:
            return Response({'error':'The order status must be in progress or the order already complated'},status=status.HTTP_409_CONFLICT)
    
    

#####Trip


class DriverNewTripListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        driver=Driver.objects.get(phone=request.user.phone)
        trips = Trip.objects.filter(driver__isnull=True,status=Status.PENDING,car__car_category=driver.carCategory)
        serializer = DriverTripListSerializer(trips, many=True)
        return Response(serializer.data)


class DriverCurrentTripsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trips = Trip.objects.filter(
            Q(driver=request.user) &
            (Q(status='IN_PROGRESS') | Q(status='PENDING'))
        )
        serializer = DriverTripListSerializer(trips, many=True)
        return Response(serializer.data)


class DriverPreviousTripsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        completed_trips = Trip.objects.filter(driver=request.user, status='COMPLETED')
        completed_trips_serializer = DriverTripListSerializer(completed_trips, many=True)

        cancelled_trips = Trip.objects.filter(driver=request.user, status='CANCELLED')
        cancelled_trips_serializer = DriverTripListSerializer(cancelled_trips, many=True)

        rejected_trips = Trip.objects.filter(driver=request.user, status='REJECTED')
        rejected_trips_serializer = DriverTripListSerializer(rejected_trips, many=True)

        data = {
            'completed_trips': completed_trips_serializer.data,
            'cancelled_trips': cancelled_trips_serializer.data,
            'rejected_trips': rejected_trips_serializer.data
        }
        return Response(data)


class DriverStatisticsTripsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_date = date.today()
        current_month = timezone.now().month
        current_year = timezone.now().year

        today_trips = Trip.objects.filter(
            driver=request.user,
            status='COMPLETED',
            createdAt__date=current_date
        )

        month_trips = Trip.objects.filter(
            driver=request.user,
            status='COMPLETED',
            createdAt__month=current_month
        )

        year_trips = Trip.objects.filter(
            driver=request.user,
            status='COMPLETED',
            createdAt__year=current_year
        )

        today_price_sum = today_trips.aggregate(Sum('price'))['price__sum']
        month_price_sum = month_trips.aggregate(Sum('price'))['price__sum']
        year_price_sum = year_trips.aggregate(Sum('price'))['price__sum']

        serializer = DriverTripListSerializer(today_trips, many=True)

        data = {
            'today_trips': serializer.data,
            'today_price_sum': today_price_sum,
            'month_trips': DriverTripListSerializer(month_trips, many=True).data,
            'month_price_sum': month_price_sum,
            'year_trips': DriverTripListSerializer(year_trips, many=True).data,
            'year_price_sum': year_price_sum
        }

        return Response(data)
    
    
class DriverAcceptTrip(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            trip=Trip.objects.get(pk=request.data['trip_id'])
        except Trip.DoesNotExist:
            return Response({'error':'Trip does not found'},status=status.HTTP_404_NOT_FOUND)
        try:
            driver=Driver.objects.get(pk=request.user.pk)
        except Driver.DoesNotExist:
            return Response({'error':'It is not a driver account'},status=status.HTTP_404_NOT_FOUND)
        if trip.driver is None:
            trip.driver=driver
            trip.status=Status.IN_PROGRESS
            trip.save()
            return Response({'result':'Order accepted'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error':'The order was accepted by another driver'},status=status.HTTP_400_BAD_REQUEST)
        
class DriverRejectTrip(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            trip=Trip.objects.get(pk=request.data['trip_id'])
        except Trip.DoesNotExist:
            return Response({'error':'Trip does not found'},status=status.HTTP_404_NOT_FOUND)
        try:
            driver=Driver.objects.get(pk=request.user.pk)
        except Driver.DoesNotExist:
            return Response({'error':'It is not a driver account'},status=status.HTTP_404_NOT_FOUND)
        if trip.driver.phone == driver.phone:
            trip.status=Status.REJECTED
            trip.save()
            return Response({'result':'Order Rejected'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error':'The order was accepted by another driver'},status=status.HTTP_400_BAD_REQUEST)



class DriverComlateTrip(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            trip=Trip.objects.get(pk=request.data['trip_id'])
        except Trip.DoesNotExist:
            return Response({'error':'Trip does not found'},status=status.HTTP_404_NOT_FOUND)
        try:
            driver=Driver.objects.get(pk=request.user.pk)
            driver_wallet=UserWallet.objects.get(user__phone=driver.phone)
        except Driver.DoesNotExist:
            return Response({'error':'It is not a driver account'},status=status.HTTP_404_NOT_FOUND)
        except UserWallet.DoesNotExist:
            return Response({'error':'Driver does not have a wallet. '},status=status.HTTP_404_NOT_FOUND)
        if trip.driver.phone == driver.phone:
            if trip.status==Status.IN_PROGRESS:
                trip.status=Status.COMPLETED
                trip.save()
                driver_wallet.balance+=Decimal(trip.price)
                driver_wallet.save()
            else:
                return Response({'error':'The order status must be in progress or the order already complated'},status=status.HTTP_400_BAD_REQUEST)
            return Response({'result':'Order Complated'},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error':'The order was accepted by another driver'},status=status.HTTP_400_BAD_REQUEST)