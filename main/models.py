from django.db import models
from django.utils import timezone

from .forms import User
from .views import random_generator

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(
        max_length=20, default=random_generator, unique=True)
    avatar = models.ImageField(
        default="default.jpg", upload_to="profile_images")
    bio = models.CharField(max_length=160, default="Passarinho azul")
    capa = models.ImageField(default="default.jpg",
                             upload_to="background_images")

    def following(self):
        user_ids = Relationship.objects.filter(from_user=self.user)\
            .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def followers(self):
        user_ids = Relationship.objects.filter(to_user=self.user)\
            .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def __str__(self):
        return self.user.username


class Tweet(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="tweets")
    content = models.CharField(max_length=140, null=True, blank=True)
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="reply")
    retweets_the = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="retweet")
    created_on = models.DateTimeField(default=timezone.now)
    num_type = models.IntegerField(default=0)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        text = f"{self.user.user.username}: {self.content}"
        return text


class Like(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="user_like", null=True, blank=True
    )
    tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name="like")
    date = models.DateTimeField(default=timezone.now)
#    count = models.BooleanField(default=False)

    class Meta:
        unique_together = [["user", "tweet"]]

    def __str__(self):
        text = f"{self.user.user.username} | {self.tweet} | {self.date}"
        return text


class Relationship(models.Model):
    from_user = models.ForeignKey(
        User, related_name='relationships', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='related_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'
