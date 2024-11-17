from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from api.v1.mixins import CRUDMixin, ListCreateDestroyMixin
from api.v1.permissions import IsAdmin, IsAuthor
from api.v1.reviews import serializers, utils
from api.v1.reviews.filters import TitleFilter
from reviews.models import Category, Genre, Title


class CategoryViewSet(ListCreateDestroyMixin):
    """Вьюсет для работы с категориями."""

    permission_classes = (IsAdmin,)
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyMixin):
    """Вьюсет для работы с жанрами."""

    permission_classes = (IsAdmin,)
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(CRUDMixin):
    """Вьюсет для создания и отображения объектов произведений."""

    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    serializer_class = serializers.TitleSerializer

    def get_queryset(self):
        return (
            Title.objects.annotate(rating=Avg('reviews__score',))
            .order_by('id',)
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleSerializer
        return serializers.TitleCreateSerializer


class ReviewViewSet(CRUDMixin):
    """Вьюсет для создания, обновления и получения отзывов."""

    permission_classes = (IsAuthor,)
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return (
            utils.get_title_or_review(self.kwargs.get('title_id'))
            .reviews.all()
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=utils.get_title_or_review(self.kwargs['title_id'])
        )


class CommentViewSet(CRUDMixin):
    """Вьюсет для создания, обновления и получения Comment."""

    permission_classes = (IsAuthor,)
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return utils.get_title_or_review(
            self.kwargs.get('title_id'),
            self.kwargs.get('review_id'),
        ).comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=utils.get_title_or_review(
                self.kwargs['title_id'],
                self.kwargs['review_id']
            )
        )
