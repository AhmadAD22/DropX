from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

class ResturantSubscripted(BasePermission):
    message = {"error": "You must have a subscription to access this resource"}

    def has_permission(self, request, view):
        
        user = request.user
        if user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True
            if user.restaurant.restaurantSubscription:
                if user.restaurant.restaurantSubscription.is_expired():
                    self.message = {"error": "Your subscription has expired, please renew."}
                    return False
                if user.restaurant.restaurantSubscription.enabled==False:
                    self.message = {"error": "You must have an active subscription to access this resource"}
                    return False
                elif user.restaurant.restaurantSubscription.paid==False:
                    self.message = {"error": "You must pay the subscription."}
                else:
                    return True
            else:
                return False
        else:
            self.message = {"error": "You are not authenticated"}
            return False
        
        

class DriverOrderSubscripted(BasePermission):
    message = {"error": "You must have a subscription to access this resource"}

    def has_permission(self, request, view):
        
        user = request.user
        if user.is_authenticated:
            if user.driver.driverOrderSubscription:
                if user.driver.driverOrderSubscription.is_expired():
                    self.message = {"error": "Your order subscription has expired, please renew."}
                    return False
                if user.driver.driverOrderSubscription.enabled==False:
                    self.message = {"error": "You must have an active order subscription to access this resource"}
                    return False
                elif user.driver.driverOrderSubscription.paid==False:
                    self.message = {"error": "You must pay the order subscription."}
                else:
                    return True
            else:
                return False
        else:
            self.message = {"error": "You are not authenticated"}
            return False
        
        
class DriverTripSubscripted(BasePermission):
    message = {"error": "You must have a subscription to access this resource"}

    def has_permission(self, request, view):
        
        user = request.user
        if user.is_authenticated:
            if user.driver.driverTripSubscription:
                if user.driver.driverTripSubscription.is_expired():
                    self.message = {"error": "Your People transport subscription has expired, please renew."}
                    return False
                if user.driver.driverTripSubscription.enabled==False:
                    self.message = {"error": "You must have an active People transport subscription to access this resource"}
                    return False
                elif user.driver.driverTripSubscription.paid==False:
                    self.message = {"error": "You must pay the People transport subscription."}
                else:
                    return True
            else:
                return False
        else:
            self.message = {"error": "You are not authenticated"}
            return False