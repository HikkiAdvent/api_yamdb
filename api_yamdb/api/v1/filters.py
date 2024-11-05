from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    """Фильтр выборки произведений по определенным полям."""

    class Meta:
        model = Title
        filterset_fields = {
            'category__slug': ['icontains'],
            'genre__slug': ['icontains'],
            'name': ['icontains'],
            'year': ['exact'],
        }
