from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_year

User = get_user_model()


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(verbose_name='Название жанра',
                            max_length=50, unique=True)
    slug = models.SlugField(verbose_name='Слаг жанра', max_length=50,
                            unique=True, validators=[
                                RegexValidator(
                                    regex=r'^[-a-zA-Z0-9_]+$',
                                    message='Слаг может содержать только \
                                    латинские буквы, цифры, знак \
                                    подчеркивания и дефис.',
                                    code='invalid_slug'
                                )
                            ])

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(verbose_name='Название категории',
                            max_length=50, unique=True)
    slug = models.SlugField(verbose_name='Слаг категории',
                            max_length=50, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(verbose_name='Название произведения',
                            max_length=150, blank=False)
    year = models.IntegerField(verbose_name='Год создания',
                               validators=[validate_year], null=True)
    description = models.TextField(verbose_name='Описание произведения',
                                   null=True, blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр произведения')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 verbose_name='Категория')

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name
    

class Review(models.Model):
    text = models.CharField(max_length=200)
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    
    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    
    def __str__(self):
        return self.text
