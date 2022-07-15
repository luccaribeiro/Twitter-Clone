from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("timeline/", views.principal, name='timeline_page'),
    path("perfil/<str:username>/", views.perfil, name='perfil')
]



