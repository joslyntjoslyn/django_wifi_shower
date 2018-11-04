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


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    preheat_cycle = models.FloatField(null=True, blank=True)
    shower_cycle = models.FloatField(null=True, blank=True)
    shower_temp = models.FloatField(null=True, blank=True)
    old_shower_habits = models.FloatField(null=True, blank=True)
    water_used = models.FloatField(null=True, blank=True)
    water_saved = models.FloatField(null=True, blank=True)
    challenge_level = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_shower_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'profile'


class ShoweringData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    # 0: norma1: challenge
    shower_mode = models.IntegerField(default=0)
    preheat_cycle = models.FloatField(null=True, blank=True)
    shower_cycle = models.FloatField(null=True, blank=True)
    old_shower_habits = models.FloatField(null=True, blank=True)
    water_used = models.FloatField(null=True, blank=True)
    water_saved = models.FloatField(null=True, blank=True)
    shower_temp = models.FloatField(null=True, blank=True)
    mixing_temp = models.FloatField(null=True, blank=True)
    challenge_level = models.FloatField(null=True, blank=True)
    aggregate_water_used = models.FloatField(null=True, blank=True)
    average_water_used = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'showering_data'

