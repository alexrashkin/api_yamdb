from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import validate_username


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Модератор'),
        (MODERATOR, 'Администратор'),
    )
    role = models.CharField(
        max_length=50,
        choices=CHOICES,
        blank=False,
        default=USER,
        verbose_name='Роль'
    )
    username = models.CharField(
        validators=(validate_username, ),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Никнейм'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    confirmation_code = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        default='XXXX',
        verbose_name='Код подтверждения',
        help_text=('Введите код подтверждения,'
                   'который был отправлен на ваш email')
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self. ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


@receiver(post_save, sender=User)
def post_save(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(
            instance
        )
        instance.confirmation_code = confirmation_code
        instance.save()
