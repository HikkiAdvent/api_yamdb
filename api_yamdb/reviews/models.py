from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import MyUser


class Title(models.Model):
    ...

    # Другие поля

    rating = models.IntegerField(
        'Рейтинг',
        null=True,
        blank=True,
    )

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews:
            self.rating = int(reviews.aggregate(models.Avg('score'))['score__avg'])
        else:
            self.rating = None
        self.save()


class Review(models.Model):
    title = models.ForeignKey(
        Title, # Ссылка на модель Title
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField()
    score = models.IntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        message='Оценка должна быть от 1 до 10.'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
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
            )]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
