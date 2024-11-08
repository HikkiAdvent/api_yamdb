from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from .constants import MIN_SCORE, MAX_SCORE

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title для GET-запросов."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return None
        rating = reviews.aggregate(models.Avg('score'))
        return rating['score__avg']


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объектов Title (POST запрос)."""

    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def create(self, validated_data):
        genres_data = validated_data.pop('genre')
        category = validated_data.pop('category')
        title = Title.objects.create(**validated_data, category=category)
        title.genre.set(genres_data)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для GET запросов Review."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления Review (POST, PATCH запросы)."""

    class Meta:
        model = Review
        fields = ('text', 'score')

    def validate_score(self, value):
        if not (MIN_SCORE <= value <= MAX_SCORE):
            raise serializers.ValidationError(
                f'Оценка должна быть от {MIN_SCORE} до {MAX_SCORE}.')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для GET запросов к комментариям."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CommentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления Comment (POST, PATCH запросы)."""

    class Meta:
        model = Comment
        fields = ('text',)
