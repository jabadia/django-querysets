from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='queries-index'),
    path('first', views.first),
    path('and_operation', views.and_operation),
    path('or_operation', views.or_operation),
    path('not_equal', views.not_equal),
    path('in_filtering', views.in_filtering),
    path('is_null', views.is_null),
    path('like', views.like),
    path('comparison', views.comparison),
    path('between', views.between),
    path('limit', views.limit),
    path('orderby', views.orderby),
    path('get_single', views.get_single),
    path('joins', views.joins),
    path('annotations', views.annotations),
]
