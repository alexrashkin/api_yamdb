from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    text = models.CharField(max_length=200)
    score = models.SlugField(unique=True)
    author = 1

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
