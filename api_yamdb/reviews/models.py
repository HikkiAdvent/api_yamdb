from datetime import datetime
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
    )
from django.db import models


class Category(models.Model):
    """Класс категорий."""

    title = models.CharField(
        max_length=256,
        verbose_name='Название',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг категории содержит недопустимый символ'
        )]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)


class Genre(models.Model):
    """Класс жанров."""

    title = models.CharField(
        max_length=75,
        verbose_name='Hазвание',
        db_index=True
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг жанра содержит недопустимый символ'
        )]
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('title',)


class Title(models.Model):
    """Класс произведений."""

    title = models.CharField(
        max_length=150,
        verbose_name='Hазвание',
        db_index=True
    )
    year = models.PositiveIntegerField(
        verbose_name='год выпуска',
        validators=[
            MinValueValidator(
                0,
                message='Значение года не может быть отрицательным'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message='Значение года не может быть больше текущего'
            )
        ],
        db_index=True
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='жанр'

    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'title')


class GenreTitle(models.Model):
    """Вспомогательный класс, связывающий жанры и произведения."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )

    class Meta:
        verbose_name = 'Соответствие жанра и произведения'
        verbose_name_plural = 'Таблица соответствия жанров и произведений'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} принадлежит жанру/ам {self.genre}'
