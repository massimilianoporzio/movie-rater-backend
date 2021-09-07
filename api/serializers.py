from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Movie, Rating

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password']
        extra_kwargs = {'password':{'write_only': True, 'required':True}} # password NON LA VEDO se non quando la scrivo
         # e in piuà la devo inserire nel body se voglio usare il viewset per scrivere uno USER (creare)

    # FARE OVERRIDE PER IL CREATE PER NON SALVARE LE PASSWORD IN CHIARO
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        #ora creo Token associato
        Token.objects.create(user=user)
        return user


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description','no_of_ratings', 'avg_rating']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'stars', 'user','movie']
