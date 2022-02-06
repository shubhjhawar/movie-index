from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .models import *
from .serializers import *
from .tasks import sleepy, send_email_task
import logging
logger = logging.getLogger('django')

# Create your views here.

class AllMoviesView(GenericAPIView):  #gotta add try catch block
    def get(self, request):
        try:
            queryset = MoviesModel.objects.all().values()
            print(queryset)
            logger.info('all the movies were shown successfully')
            return Response({"movies": queryset}, status=status.HTTP_201_CREATED)
        except Exception:
            logger.info('exception occurred')
            return Response({"failure":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = MoviesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info("movie is stored in the database successfully")
                return Response({"success":"movie is saved in the database"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logger.info('exception handled')
            return Response({"failure":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

class AddUserView(GenericAPIView):
    def post(self, request):
        try:
            email = request.data.get('email','')
            user_serializer=UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                logger.info('serializer is valid')

                send_email_task.delay(email)
                logger.info('email sent successfully')

                return Response({"success": "user is added successfully"}, status=status.HTTP_201_CREATED)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            logger.info('exception occurred')
            return Response({"failure":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)



class UserView(GenericAPIView):
    def post(self, request, user_id):
        data = request.data
        movie_name = data.get('movie_name','')
        if MoviesModel.objects.filter(title=movie_name).exists():
            movie = MoviesModel.objects.get(title=movie_name)
            queryset={}
            queryset['user_info'] = user_id
            queryset['movie_info'] = movie.id
            serializer = UserMovieSerializer(data=queryset)
            if serializer.is_valid():
                serializer.save()
                logger.info("movie is bookmarked successfully")
                return Response({"success": "movie is bookmarked successfully"}, status=status.HTTP_201_CREATED)
            logger.info("something went wrong")
            return Response({"failure": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        logger.info("the movie is already in the database")
        return Response({"failure": "this movie does not exist in the database"}, status=status.HTTP_400_BAD_REQUEST)

    
    def get(self, request, user_id):
        try:
            bookmarked_movies = BookmarkMoviesModel.objects.filter(user_info=user_id)
            if bookmarked_movies:
                movie_list = []
                for i in bookmarked_movies:
                    movie =i.movie_info
                    movie_serializer = MoviesSerializer
                    movie = movie_serializer(movie)
                    movie_list.append(movie.data)
                logger.info("all the movies were displayed successfully")
                return Response(movie_list, status=status.HTTP_200_OK)
            logger.info("user has not bookmarked any movie for now.")
            return Response({"please add some movies in your list first"}, status=status.HTTP_200_OK)
        except Exception:
            logger.info('exception handled')
            return Response({"failure": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        try:
            movie_name = request.data.get('movie_name', '')
            movie_object = MoviesModel.objects.get(title=movie_name)
            movie_id = movie_object.id
            instance = BookmarkMoviesModel.objects.get(user_info=user_id, movie_info=movie_id)
            instance.delete()
            logger.info("movie is not bookmarked anymore")
            return Response({"success":"movie is not bookmarked anymore"},status=status.HTTP_200_OK)
        except Exception:
            logger.info('exception occurred')
            return Response({"failure":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)





