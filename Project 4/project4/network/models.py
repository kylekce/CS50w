from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user} posted {self.content} on {self.date}"