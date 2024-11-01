from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Title

from .permissions import (AnonimReadOnly, IsSuperUserOrIsAdminOnly)
from .serializers import (
    CategorySerializer, GenreSerializer,
    TitleGETSerializer, TitleSerializer
    )


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для создания обьектов класса Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для создания обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """Вьюсет для создания обьектов класса Title."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (AnonimReadOnly | IsSuperUserOrIsAdminOnly,)
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        return TitleGETSerializer if self.request.method == 'GET' else TitleSerializer
