from django.urls import path

from . import views

urlpatterns = [
    path('', views.binyans),
    path('verbs/', views.verbs),
]
