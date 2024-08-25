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