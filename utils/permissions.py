from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status

class ResturantSubscripted(BasePermission):
    message = "You must have an active subscription to access this resource."

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.restaurant.restaurantSubscription:
            return True
        else:
            response_data = {'error': self.message}
            response = Response(response_data, status=status.HTTP_403_FORBIDDEN)
            return response