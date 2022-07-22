from django.contrib import admin
from .models import Profile, Tweet, Like
# Register your models here.
# admin.site.register(Retweet)
admin.site.register(Profile)
admin.site.register(Tweet)
admin.site.register(Like)