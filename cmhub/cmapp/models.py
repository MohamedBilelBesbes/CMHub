from django.db import models

class User (models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    position = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    numberoffollowers = models.IntegerField()
    numberoffollowing = models.IntegerField()
    numberoftweets = models.IntegerField()
    content = models.CharField(max_length=1000)
    picture = models.BooleanField(default=False)
    video = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.contacted