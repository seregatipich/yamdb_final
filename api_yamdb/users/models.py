from dataclasses import dataclass

from django.contrib.auth.models import AbstractUser
from django.db import models


@dataclass
class UserRole:
    USER: str = 'user'
    MODERATOR: str = 'moderator'
    ADMIN: str = 'admin'


ROLE_CHOICES = (
    (UserRole.USER, 'Пользователь'),
    (UserRole.MODERATOR, 'Модератор'),
    (UserRole.ADMIN, 'Администратор'),
)


class User(AbstractUser):
    """
    Модель для создания пользователя.
    """
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=UserRole.USER,
        blank=True,
        verbose_name='Роль',
    )
    email = models.EmailField('Электронная почта', max_length=254, unique=True)
    bio = models.TextField(
        max_length=1024,
        blank=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Код подтверждения',
    )

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == UserRole.USER

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
