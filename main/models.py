from django.utils import timezone
from django.db import models
from .forms import User
from .views import random_generator


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=160, default=random_generator, unique=True)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.CharField(max_length=160, default='Passarinho azul')

    def __str__(self):
        return self.user.username


class Tweet(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="tweets")
    content = models.CharField(max_length=140)
    created_on = models.DateTimeField(default=timezone.now)
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, related_name="reply", null=True, blank=True)

    class Meta():
        ordering = ['created_on']

    def __str__(self):
        text = f'{self.user.user.username}: {self.content}'
        return text

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="like", null=True, blank=True)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE, related_name="like")
    count = models.BooleanField(default=False)

    def __str__(self):
        text = f'{self.user.user.username} | {self.tweet} | {self.count}'
        return text