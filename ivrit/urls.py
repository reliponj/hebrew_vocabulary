from django.urls import path

from ivrit import views

urlpatterns = [
    path('', views.index, name="index"),
    path('privacy/', views.privacy, name="privacy"),
    path('change_filter/<param>/<value>/', views.change_filter, name='change_filter'),

    path('api/vocabulary/', views.api_vocabulary),
    path('api/kluch/', views.api_kluch),
    path('api/settings/', views.api_settings),
]
