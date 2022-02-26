from xml.parsers.expat import model
from django.db import models
#from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, blank=False)
    username = models.CharField(blank=True, unique=False, max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return super().get_full_name() or self.email


class Todo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Status(models.TextChoices):
        NOT_STARTED = 'notStarted'
        ON_GOING = 'onGoing'
        COMPLETED = 'completed'

    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.NOT_STARTED)
