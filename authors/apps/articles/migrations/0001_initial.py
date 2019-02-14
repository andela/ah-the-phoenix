# Generated by Django 2.1.5 on 2019-02-13 22:06

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=400)),
                ('body', models.TextField()),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField(blank=True, max_length=1000, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
