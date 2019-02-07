from django.db import models
from cloudinary.models import CloudinaryField

from django.db.models.signals import post_save
from django.dispatch import receiver

from ..authentication.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    image = CloudinaryField("image",
        default="https://res.cloudinary.com/dw675k0f5/image/upload/v1542660993/sample.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        Profile.objects.create(user=instance)
        instance.profile.save()