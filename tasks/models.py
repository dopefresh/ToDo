from django.db import models
from django.utils import timezone
from django.conf import settings




class Group(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
