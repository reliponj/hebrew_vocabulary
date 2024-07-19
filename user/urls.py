from django.urls import path

from user import views

urlpatterns = [
    path('welcome/', views.welcome, name="welcome"),
    path('login/', views.login, name="login"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('logout/', views.logout, name="logout"),

    path('profile/', views.profile, name="profile"),
]
