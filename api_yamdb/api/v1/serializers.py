from rest_framework import serializers, validators
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import models
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Genre, Title, Comment, Review

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
    """Сериализатор объектов класса Title."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    raiting = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        validators = (
            validators.UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('author', 'title',)
            ),
        )

    def create(self, validated_data):
        genres_data = validated_data.pop('genre')
        category_data = validated_data.pop('category')
        category = Category.objects.get(slug=category_data['slug'])
        validated_data['category'] = category
        title = Title.objects.create(**validated_data)
        genre_slugs = [genre['slug'] for genre in genres_data]
        genres = Genre.objects.filter(slug__in=genre_slugs)
        title.genre.set(genres)
        return title

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            category_data = validated_data.pop('category')
            instance.category = Category.objects.get(
                slug=category_data['slug']
            )
        if 'genre' in validated_data:
            genres_data = validated_data.pop('genre')
            genre_slugs = [genre['slug'] for genre in genres_data]
            genres = Genre.objects.filter(slug__in=genre_slugs)
            instance.genre.set(genres)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return None
        rating = reviews.aggregate(models.Avg('score'))
        return rating['score__avg']


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        queryset=Title.objects.all(),
        slug_field='name',
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10.'
            )
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST' and Review.objects.filter(
            title=title, author=author
        ).exists():
            raise ValidationError(
                'Можно оставлять только один отзыв на произведение.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        exclude = ('review',)
