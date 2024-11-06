from rest_framework import response, status


class NoPutAPIViewMixin:
    """Миксин для запрета метода PUT."""
    def put(self, request, *args, **kwargs):
        return response.Response(
            {'detail': 'Метод PUT не разрешен.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
