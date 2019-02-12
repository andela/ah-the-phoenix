from django.db import models
from django.contrib.auth import get_user_model
from authors.apps.authentication.models import User

# Create your models here.


class Friend(models.Model):
    """
    This class defines  friend objects that will show which user follows who
    """

    follower = models.ForeignKey(
        User,
        related_name='rel_from_set',
        on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User,
        related_name='rel_to_set',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        unique_together = ('follower', 'followed')

    def __str__(self):
        """This method returns a human readable form of class object"""
        return f"{self.follower.username} follows {self.followed.username}"


get_user_model().add_to_class('following', models.ManyToManyField(
    'self', through=Friend,
    related_name='followers',
    symmetrical=False
))
