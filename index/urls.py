from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', AllMoviesView.as_view()),
    path('add_user',AddUserView.as_view()),
    path('movies/<int:user_id>',UserView.as_view()),
]