from django.contrib import admin
from .models import Profile, Tweet, Like, Comentarios

# Register your models here.
admin.site.register(Comentarios)
admin.site.register(Profile)
admin.site.register(Tweet)
admin.site.register(Like)