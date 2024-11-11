from rest_framework import response


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
