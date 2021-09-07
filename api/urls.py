from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter() #URLS PER REST API

urlpatterns = [
    path('',include(router.urls))
]