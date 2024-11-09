from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.contrib.auth import get_user_model
from django.db import models

from reviews.validators import validate_year
from reviews.constants import RETURN_TEXT_LENGTH, NAME_LENGTH

User = get_user_model()


class Category(models.Model):
    """Класс категорий."""

    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Название',
        db_index=True
    )
    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)

    def __str__(self):
        return self.name[:RETURN_TEXT_LENGTH]


class Genre(models.Model):
    """Класс жанров."""

    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Hазвание',
        db_index=True
    )
    slug = models.SlugField(
        verbose_name='slug',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id',)

    def __str__(self):
        return self.name[:RETURN_TEXT_LENGTH]


class Title(models.Model):
    """Класс произведений."""

    name = models.CharField(
        max_length=NAME_LENGTH,
        verbose_name='Hазвание',
        db_index=True
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='год выпуска',
        validators=[validate_year],
        db_index=True,
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='категория',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('id',)

    def __str__(self):
        return self.name[:RETURN_TEXT_LENGTH]


class Review(models.Model):
    """Класс отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        'оценка',
        validators=(
            MinValueValidator(
                1,
                message='Оценка должна быть не меньше 1'
            ),
            MaxValueValidator(
                10,
                message='Оцена должна быть не больше 10'
            )
        ),
    )
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв',
        verbose_name_plural = 'Отзывы',
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]
        default_related_name = 'reviews'
        ordering = ('pub_date',)

    def __str__(self):
        return (
            f'{self.author.username}: {self.title.name[:RETURN_TEXT_LENGTH]}'
        )


class Comment(models.Model):
    """Класс комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('pub_date',)

    def __str__(self):
        return (
            f'{self.author.username}: {self.text[:RETURN_TEXT_LENGTH]}'
        )
