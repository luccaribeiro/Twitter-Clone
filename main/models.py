from django.utils import timezone
from django.db import models
from .forms import User

# Create your models here.


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    content = models.CharField(max_length=140)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like", null=True, blank=True)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE, related_name="like")
    count = models.BooleanField(default=False)



    def __str__(self):
        text = f'{self.tweet} | {self.count}'
        return text