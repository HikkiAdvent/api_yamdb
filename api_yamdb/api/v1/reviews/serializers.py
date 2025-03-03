from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.v1.constants import MAX_SCORE_VALUE, MIN_SCORE_VALUE
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

    def validate_score(self, value):
        if not (MIN_SCORE_VALUE <= value <= MAX_SCORE_VALUE):
            raise serializers.ValidationError('Оценка должна быть от 1 до 10.')
        return value

    def validate(self, data):
        """Проверяет, что у пользователя только один отзыв на произведение."""

        request = self.context.get('request')
        if request and request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            user = request.user
            if Review.objects.filter(title_id=title_id, author=user).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для GET запросов к комментариям."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
