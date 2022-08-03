from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("timeline/", views.principal, name="timeline_page"),
    path("perfil/<str:username>/", views.perfil, name="perfil"),
    path("perfil/edit/<str:username>/", views.edit_perfil, name="edit.perfil"),
    path("postagem/<int:id>/", views.postagem, name="postagem"),
    path("retweet/<int:id>/", views.repost, name="retweet"),
    path("like/<int:id>/", views.like, name="like"),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
