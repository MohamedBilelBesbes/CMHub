from django.db import models



class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    numberoffollowers = models.IntegerField()
    numberoffollowing = models.IntegerField()
    numberoftweets = models.IntegerField()
    content = models.CharField(max_length=1000)
    picture = models.BooleanField(default=False)
    video = models.BooleanField(default=False)
    owner = models.CharField(max_length=200)
    def __str__(self):
        return self.contacted