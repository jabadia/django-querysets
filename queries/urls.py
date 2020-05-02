from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('first', views.first),
    path('and_operation', views.and_operation),
    path('or_operation', views.or_operation),
]
