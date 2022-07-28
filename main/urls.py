from django.urls import path, include
from . import views

app_name = "main"


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('', include('timeline.urls')),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
]
