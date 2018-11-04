import os
from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    mac_id = models.CharField(max_length=100, unique=True)
    secret_key = models.CharField(max_length=8, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    sold_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'device'



