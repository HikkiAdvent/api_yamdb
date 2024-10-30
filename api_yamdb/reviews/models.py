from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Импорт Title и User


class Review(models.Model):
    title = models.ForeignKey(
        Title, # Ссылка на модель Title
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User, # Ссылка на модель User
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField()
    score = models.IntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    ),
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв',
        verbose_name_plural = 'Отзывы',

    def __str__(self):
        return self.text
