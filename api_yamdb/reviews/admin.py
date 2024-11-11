from django.contrib import admin
from django.db.models import Avg

from reviews.constants import LIST_PER_PAGE
from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс настройки раздела категорий."""

    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Класс настройки раздела жанров."""

    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Класс настройки раздела произведений."""

    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'get_genre',
        'count_reviews',
        'get_rating'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = LIST_PER_PAGE
    search_fields = ('name', 'year', 'category')

    @admin.display(description='Жанр/ы произведения')
    def get_genre(self, object):
        """Получает жанр или список жанров произведения."""
        return '\n'.join((genre.name for genre in object.genre.all()))

    @admin.display(description='Количество отзывов')
    def count_reviews(self, object):
        """Вычисляет количество отзывов на произведение."""
        return object.reviews.count()

    @admin.display(description='Рейтинг')
    def get_rating(self, object):
        """Вычисляет рейтинг произведения."""
        rating = object.reviews.aggregate(average_score=Avg('score'))
        return round(rating.get('average_score'), 1)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Класс настройки раздела отзывы."""

    list_display = (
        'id',
        'title',
        'author',
        'score',
        'pub_date',
    )
    list_filter = ('author',)
    empty_value_display = 'значение отсутствует'
    list_per_page = LIST_PER_PAGE
    search_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс настройки раздела комментарий."""

    list_display = (
        'id',
        'review',
        'author',
        'text',
        'pub_date',
    )
    list_filter = ('author',)
    empty_value_display = 'значение отсутствует'
    list_per_page = LIST_PER_PAGE
    search_fields = ('author',)
