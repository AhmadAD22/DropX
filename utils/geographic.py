from geopy.distance import geodesic
from accounts.models import Restaurant
from client.serializers.restaurant_serializer import RestaurantListSerializer

def get_nearest_restaurants(client_latitude, client_longitude,restaurants):
    # restaurant = Restaurant.objects.filter(id__in=restaurant_ids)
    restaurant_with_distance = []

    for restaurant in restaurants:
       restaurant_latitude =restaurant.restaurant.latitude
       restaurant_longitude = restaurant. restaurant.longitude

       if restaurant_latitude and restaurant_longitude:
            restaurant_location = (restaurant_latitude, restaurant_longitude)
            client_location = (client_latitude, client_longitude)
            distance = geodesic(restaurant_location, client_location).kilometers
            restaurant_with_distance.append((restaurant, distance))
    restaurant_with_distance.sort(key=lambda x: x[1])  # Sort restaurant by distance 
    # return the stors and their distance
    ordered_stors = [{'restaurant':RestaurantListSerializer(restaurant).data,'distance':distance} for restaurant, distance in restaurant_with_distance]
    return ordered_stors



def calculate_distance(sourceLat, sourceLon, destenationLat, destenationLon):
    # Define the coordinates of the two points
    sourcePoint = (sourceLat, sourceLon)
    destenationPoint = (destenationLat, destenationLon)

    # Calculate the distance using Geopy
    dist = geodesic(sourcePoint, destenationPoint).kilometers

    return dist