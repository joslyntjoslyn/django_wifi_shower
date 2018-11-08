import os
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Device(models.Model):
    mac_id = models.CharField(max_length=100, unique=True)
    secret_key = models.CharField(max_length=8, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    sold_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'device'

    def save(self, *args, **kwargs):
        self.secret_key = os.urandom(4).hex()
        super(Device, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    last_shower_date = models.DateTimeField(null=True, blank=True)
    old_shower_habits = models.FloatField(null=True, blank=True)
    shower_cycle = models.FloatField(null=True, blank=True)
    gallons_saved = models.FloatField(null=True, blank=True)
    shower_temp = models.FloatField(null=True, blank=True)
    challenge_level = models.FloatField(null=True, blank=True)
    shower_count = models.IntegerField(default=0)
    average_shower_time = models.FloatField(default=0)
    aggregate_shower_savings = models.FloatField(default=0)

    class Meta:
        db_table = 'profile'


class ShoweringData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    # 0: norma1: challenge
    shower_mode = models.IntegerField(default=0)
    preheat_cycle = models.FloatField(null=True, blank=True)
    old_shower_habits = models.FloatField(null=True, blank=True)
    shower_cycle = models.FloatField(null=True, blank=True)
    shower_temp = models.FloatField(null=True, blank=True)
    gallons_used = models.FloatField(null=True, blank=True)
    gallons_saved = models.FloatField(null=True, blank=True)
    average_shower_time = models.FloatField(null=True, blank=True)
    aggregate_shower_savings = models.FloatField(null=True, blank=True)
    average_shower_savings = models.FloatField(null=True, blank=True)
    challenge_level = models.FloatField(null=True, blank=True)
    challenge_time = models.FloatField(null=True, blank=True)
    # False: started, True: ended
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'showering_data'

