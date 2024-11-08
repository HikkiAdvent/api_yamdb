from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, Genre, Review, Title

from api.v1.reviews import serializers
from api.v1.reviews.filters import TitleFilter
from api.v1.reviews.permissions import IsAdmin, IsAuthor


class CategoryViewSet(ModelViewSet):
    """Вьюсет для работы с категориями."""
    permission_classes = (IsAdmin,)
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST', 'DELETE'])

    def partial_update(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST', 'DELETE'])


class GenreViewSet(ModelViewSet):
    """Вьюсет для работы с жанрами."""
    permission_classes = (IsAdmin,)
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST', 'DELETE'])

    def partial_update(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST', 'DELETE'])


class TitleViewSet(ModelViewSet):
    """Вьюсет для создания и отображения объектов произведений."""
    queryset = Title.objects.all()
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TitleSerializer
        return serializers.TitleCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.save()
        response_serializer = serializers.TitleSerializer(
            title,
            context={'request': request}
        )
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data, partial=partial
        )
        serializer.is_valid(
            raise_exception=True
        )
        title = serializer.save()
        response_serializer = serializers.TitleSerializer(
            title,
            context={'request': request}
        )
        return Response(response_serializer.data)


class ReviewViewSet(ModelViewSet):
    """Вьюсет для создания, обновления и получения отзывов."""
    permission_classes = (IsAuthor,)
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs['title_id'])
        )
        response_serializer = serializers.ReviewSerializer(
            review, context={'request': request}
        )
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        review = serializer.save()

        response_serializer = serializers.ReviewSerializer(
            review,
            context={'request': request}
        )
        return Response(response_serializer.data)


class CommentViewSet(ModelViewSet):
    """Вьюсет для создания, обновления и получения Comment."""
    permission_classes = (IsAuthor,)
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.CommentSerializer
        return serializers.CommentCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs['review_id'])
        )
        response_serializer = serializers.CommentSerializer(
            comment,
            context={'request': request}
        )
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        response_serializer = serializers.CommentSerializer(
            comment,
            context={'request': request}
        )
        return Response(response_serializer.data)
