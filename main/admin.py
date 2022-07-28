from django.contrib import admin
from .models import Profile, Tweet, Like, Retweet, Reply
# Register your models here.
# admin.site.register(Retweet)
admin.site.register(Profile)
admin.site.register(Tweet)
admin.site.register(Retweet)
admin.site.register(Reply)
admin.site.register(Like)
