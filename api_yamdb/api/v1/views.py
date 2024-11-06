from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from reviews.models import Category, Genre, Title, Review
from api.v1.permissions import (
    IsAuthor,
    IsAdmin
)
from api.v1.serializers import (
    CategorySerializer, GenreSerializer,
    TitleSerializer, ReviewSerializer,
    CommentSerializer
)


class CategoryViewSet(ModelViewSet):
    """Вьюсет для создания обьектов класса Category."""
    permission_classes = (IsAdmin,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_field = ('name',)


class GenreViewSet(ModelViewSet):
    """Вьюсет для создания обьектов класса Genre."""
    permission_classes = (IsAdmin,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_field = ('name',)


class TitleViewSet(ModelViewSet):
    """Вьюсет для создания обьектов класса Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
        title.update_rating()

    def perform_update(self, serializer):
        serializer.save()
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        title.update_rating()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthor,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
