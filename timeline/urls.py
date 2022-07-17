from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path("timeline/", views.principal, name='timeline_page'),
    path("perfil/<str:username>/", views.perfil, name='perfil')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



