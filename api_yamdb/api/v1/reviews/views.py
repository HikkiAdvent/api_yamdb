from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, mixins, viewsets

from api.v1.reviews import serializers
from api.v1.reviews.filters import TitleFilter
from api.v1.reviews.mixins import PatchModelMixin
from api.permissions import IsAdmin, IsAuthor
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для работы с категориями."""

    permission_classes = (IsAdmin,)
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для работы с жанрами."""

    permission_classes = (IsAdmin,)
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(
    PatchModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для создания и отображения объектов произведений."""

    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_queryset(self):
        return (
            Title.objects.annotate(rating=Avg('reviews__score',))
            .order_by('id',)
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleSerializer
        return serializers.TitleCreateSerializer


class ReviewViewSet(
    PatchModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для создания, обновления и получения отзывов."""

    permission_classes = (IsAuthor,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ReviewSerializer
        return serializers.ReviewCreateSerializer

    def create(self, request, *args, **kwargs):
        if Review.objects.filter(
            title=self.kwargs['title_id'],
            author=self.request.user
        ).exists():
            raise exceptions.ValidationError(
                'Вы уже оставили отзыв на это произведение.'
            )
        return super().create(request, *args, **kwargs)


class CommentViewSet(
    PatchModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для создания, обновления и получения Comment."""

    permission_classes = (IsAuthor,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.CommentSerializer
        return serializers.CommentCreateSerializer
