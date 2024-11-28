from django.urls import path

from . import views

urlpatterns = [
    path('', views.binyans),
    path('verbs/', views.verbs),
    path('verbs/by_search/', views.verb_by_search),
]
