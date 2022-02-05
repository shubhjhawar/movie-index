from django.db import models

# Create your models here.

class MoviesModel(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
    director = models.CharField(max_length=100, blank=True)
    writer = models.CharField(max_length=100, blank=True)

class UserModel(models.Model):
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email = models.EmailField()
    password = models.CharField(max_length=30)


class BookmarkMoviesModel(models.Model):
    user_info = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    movie_info = models.ForeignKey(MoviesModel, on_delete=models.CASCADE)

    




