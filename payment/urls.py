from django.urls import path

from payment import views

urlpatterns = [
    path('create/', views.create, name="pay_create"),
    path('callback/', views.callback, name="pay_callback"),
    # path('trial/', views.trial, name="pay_trial"),
]
