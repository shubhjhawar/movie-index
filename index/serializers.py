from rest_framework import serializers
from .models import *


class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model=MoviesModel
        fields='__all__'

    def validate(self, attrs):
        title =attrs.get('title','')

        if MoviesModel.objects.filter(title=title).exists():
            raise serializers.ValidationError({"title error":"movie already exists in the database"})

        return super().validate(attrs)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModel
        fields='__all__'

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        # if UserModel.objects.filter(email=email).exists():
        #     raise serializers.ValidationError({'email_error': "email already exists"})
        if UserModel.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username_error': "username already exists"})

        return super().validate(attrs)


class UserMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookmarkMoviesModel
        fields = ['user_info','movie_info']