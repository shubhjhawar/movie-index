from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .models import *
from .serializers import *
from .tasks import sleepy, send_email_task


# Create your views here.

class AllMoviesView(GenericAPIView):  #gotta add try catch block
    def get(self, request):
        queryset = MoviesModel.objects.all().values()
        print(queryset)
        return Response({"movies": queryset}, status=status.HTTP_201_CREATED)


    def post(self, request):
        serializer = MoviesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"movie is saved in the database"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddUserView(GenericAPIView):
    def post(self, request):
        email = request.data.get('email','')
        user_serializer=UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            send_email_task(email)
            return Response({"success": "user is added successfully"}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        send_email_task()
        return Response({"success": "email is sent successfully"}, status=status.HTTP_200_OK)

class UserView(GenericAPIView):
    def post(self, request, user_id):
        data = request.data
        movie_name=data.get('movie_name','')
        if MoviesModel.objects.filter(title=movie_name).exists():
            movie = MoviesModel.objects.get(title=movie_name)
            queryset={}
            queryset['user_info'] = user_id
            queryset['movie_info'] = movie.id
            serializer = UserMovieSerializer(data=queryset)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": "movie is bookmarked successfully"}, status=status.HTTP_201_CREATED)
            return Response({"failure":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"failure":"this movie does not exist in the database"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, user_id):
        bookmarked_movies = BookmarkMoviesModel.objects.filter(user_info=user_id)
        if bookmarked_movies:
            movie_list =[]
            for i in bookmarked_movies:
                movie =i.movie_info
                movie_serializer = MoviesSerializer
                movie = movie_serializer(movie)
                movie_list.append(movie.data)
            return Response(movie_list, status=status.HTTP_200_OK)
        return Response({"failure": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        movie_name = request.data.get('movie_name', '')
        movie_object = MoviesModel.objects.get(title=movie_name)
        movie_id = movie_object.id
        instance = BookmarkMoviesModel.objects.get(user_info=user_id, movie_info=movie_id)
        instance.delete()
        return Response({"success":"movie is not bookmarked anymore"},status=status.HTTP_200_OK)





