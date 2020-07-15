from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import datetime


class User(models.Model):
    username = models.CharField(max_length=255, unique=True, blank=True,
                                null=True)
    age = models.PositiveIntegerField()
    active = models.BooleanField()
