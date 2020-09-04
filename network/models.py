from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    userp = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=3000)
    timestamp = models.DateTimeField(auto_now_add=True)
    userl = models.ManyToManyField(User, null=True)

    def is_ulike(self,usern):
        if usern in self.userl.all():
            return True
        else:
            return False

class Follower(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name="follow")
    following = models.ManyToManyField(User, null=True, blank=True)