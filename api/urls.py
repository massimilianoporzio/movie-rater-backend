from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import MovieViewSet, RatingViewSet

router = routers.DefaultRouter() #URLS PER REST API
router.register('movies',MovieViewSet)
router.register('ratings',RatingViewSet)

urlpatterns = [
    path('',include(router.urls))
]