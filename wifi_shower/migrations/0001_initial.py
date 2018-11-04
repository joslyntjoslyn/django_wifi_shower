# Generated by Django 2.1.3 on 2018-11-04 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_id', models.CharField(max_length=100, unique=True)),
                ('secret_key', models.CharField(max_length=8, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('sold_date', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'device',
            },
        ),
    ]
