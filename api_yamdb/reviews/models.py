from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    password = None
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email'
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=9,
        choices=USER_ROLE_CHOICES,
        default=USER
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'username',
                    'email'
                ],
                name='unique user'
            )
        ]
