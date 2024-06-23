
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Category
from ..serializers.store_serializers import *
from rest_framework.permissions import IsAuthenticated
from utils.error_handle import error_handler


###########Restaurant Data view####################################

class RestaurantDataAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        try:
            restaurant = Restaurant.objects.get(phone=request.user.phone)   
        except Restaurant.DoesNotExist:
              return Response({"erorr":"Restaurant Does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantDataSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    


########################Restaurant Opening Views###################

class RestaurantOpeningListCreateAPIView(APIView):
    def get(self, request):
        try:
            restaurant=Restaurant.objects.get(phone=request.user.phone)
        except Restaurant.DoesNotExist:
            return Response({"erorr":"Restaurant Does not exist"}, status=status.HTTP_404_NOT_FOUND)
        openings = RestaurantOpening.objects.filter(restaurant=restaurant)
        serializer = RestaurantOpeningSerializer(openings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RestaurantOpeningSerializer(data=request.data)
        try:
            restaurant=Restaurant.objects.get(phone=request.user.phone)
        except Restaurant.DoesNotExist:
            return Response({"erorr":"Restaurant Does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

class RestaurantOpeningRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, pk):
        try:
            opening = RestaurantOpening.objects.get(pk=pk)
        except RestaurantOpening.DoesNotExist:
            return Response({"erorr":"Restaurant Open time Does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantOpeningSerializer(opening)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            opening = RestaurantOpening.objects.get(pk=pk)
        except RestaurantOpening.DoesNotExist:
            return Response({"erorr":"Restaurant Open time Does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantOpeningSerializer(opening, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(error_handler(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            opening = RestaurantOpening.objects.get(pk=pk)
        except RestaurantOpening.DoesNotExist:
            return Response({"erorr":"Restaurant Open time Does not exist"}, status=status.HTTP_404_NOT_FOUND)
        opening.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

########################Common Question  Views###################

class CommonQuestionListCreateAPIView(APIView):
    def get(self, request):
        try:
            restaurant = Restaurant.objects.get(phone=request.user.phone)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        common_questions = CommonQuestion.objects.filter(restaurant=restaurant)
        serializer = CommonQuestionSerializer(common_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CommonQuestionSerializer(data=request.data)
        try:
            restaurant = Restaurant.objects.get(phone=request.user.phone)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommonQuestionRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, pk):
        try:
            common_question = CommonQuestion.objects.get(pk=pk)
        except CommonQuestion.DoesNotExist:
            return Response({"error": "Common question does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommonQuestionSerializer(common_question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            common_question = CommonQuestion.objects.get(pk=pk)
        except CommonQuestion.DoesNotExist:
            return Response({"error": "Common question does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommonQuestionSerializer(common_question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            common_question = CommonQuestion.objects.get(pk=pk)
        except CommonQuestion.DoesNotExist:
            return Response({"error": "Common question does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        common_question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

########################Reviews Views###################

class RestaurantReviewsAPIView(APIView):
    def get(self, request):
        try:
            restaurant = Restaurant.objects.get(phone=request.user.phone)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        reviews = Review.objects.filter(restaurant=restaurant)
        ratings = [review.rating for review in reviews]
        average_rating = sum(ratings) / len(ratings) if ratings else 0
        rating={
            "average": average_rating,
            "count":reviews.count()
        }
        serializer = ReviewsStorSerializer(reviews, many=True)
        return Response({"reviews":serializer.data,"rating":rating}, status=status.HTTP_200_OK)