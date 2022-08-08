from django.contrib import admin

from .models import Like, Profile, Relationship, Tweet, Notification

# Register your models here.
# admin.site.register(Retweet)
admin.site.register(Profile)
admin.site.register(Tweet)
admin.site.register(Like)
admin.site.register(Relationship)
admin.site.register(Notification)
