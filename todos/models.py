from django.contrib.auth.models import User
from django.db import models


class Todo(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.user.username} - {self.text}'
