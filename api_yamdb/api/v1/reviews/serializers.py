from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.v1.reviews.constants import MAX_SCORE_VALUE, MIN_SCORE_VALUE
from reviews.models import Category, Comment, Genre, Review, Title

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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


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
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для GET запросов Review."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
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
        if not (MIN_SCORE_VALUE <= value <= MAX_SCORE_VALUE):
            raise serializers.ValidationError('Оценка должна быть от 1 до 10.')
        return value

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        validated_data['title'] = get_object_or_404(
            Title,
            id=self.context['view'].kwargs['title_id']
        )
        return super().create(validated_data)

    def to_representation(self, instance):
        return ReviewSerializer(instance, context=self.context).data


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

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        validated_data['review'] = get_object_or_404(
            Review,
            id=self.context['view'].kwargs['review_id']
        )
        return super().create(validated_data)

    def to_representation(self, instance):
        return CommentSerializer(instance, context=self.context).data
