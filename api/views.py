from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer

User = get_user_model()

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [AllowAny] # TUTTI VEDONO E SCRIVONO
    permission_classes = [IsAuthenticated]  # TUTTI VEDONO E SCRIVONO

    #custom method for let users rating the movie via API
    # detatil=True vuole dire che funziona sul SINGOLO movie non sulla lista di tutit i movie
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            stars = request.data['stars']

            movie = Movie.objects.get(pk=pk)

            # user = User.objects.get(id=1) # per ora è fisso poi lo prenderò dalla request
            user = request.user
            print('user is: ', user)
            if(user.is_anonymous):
                response = {'message': "User MUST have been authenticated!"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            try:
                stars = int(stars)
                if stars > 5 or stars < 1:
                    raise Exception('NOT A VALID INTEGER')
            except:
                response = {'message': "Stars has to be an integer between 1 and 5"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            # guardo se c'è un rating con quello user e quel movie
            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': "Rating updated",
                            'result': serializer.data}
                return Response(response, status=status.HTTP_206_PARTIAL_CONTENT)
            except:
                rating = Rating.objects.create(user=user, movie=movie,stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': "Rating created",
                            'result': serializer.data}
                return Response(response, status=status.HTTP_201_CREATED)

        else:
            response = {'message': "You need to provide stars"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)





class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] # SOLO GLI AUTENTICATI METTONO I VOTI

    # BLOCCO PERCHé LO SI FA SOLO DALL'API MOVIE
    def update(self, request, *args, **kwargs):
        response = {'message': "You cannot update rating like that"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        response = {'message': "You cannot create rating like that"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)