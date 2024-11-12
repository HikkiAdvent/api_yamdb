from rest_framework import response
from rest_framework import mixins, viewsets


class PatchModelMixin:
    """Миксим только для частичного обновления."""

    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


class ListCreateDestroyMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Базовый вьюсет с действиями для списка,
    создания и удаления объектов.
    """
    pass


class ListRetrieveCreateDestroyMixin(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Базовый вьюсет с действиями для списка,
    получения, обновления и удаления объектов.
    """
    pass
