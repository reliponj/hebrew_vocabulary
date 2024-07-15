from django.urls import path

from ivrit import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('logout/', views.logout, name="logout"),

    path('change_filter/<param>/<value>/', views.change_filter, name='change_filter'),
]
