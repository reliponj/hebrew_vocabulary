from django.urls import path

from ivrit import views, views_verb_api

urlpatterns = [
    path('', views.index, name="index"),
    path('privacy/', views.privacy, name="privacy"),
    path('change_filter/<param>/<value>/', views.change_filter, name='change_filter'),

    path('api/vocabulary/', views.api_vocabulary),
    path('api/kluch/', views.api_kluch),
    path('api/settings/', views.api_settings),

    path('api/roots/', views_verb_api.api_root),
    path('api/roots/vocabulary/by_search/', views_verb_api.api_root_vocabulary_by_search),
    path('api/roots/vocabulary/by_root/', views_verb_api.api_root_vocabulary_by_root),
    path('api/roots/verb/', views_verb_api.api_verb),
]
