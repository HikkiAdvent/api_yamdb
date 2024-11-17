from django.shortcuts import get_object_or_404
from reviews.models import Title, Review


def get_title_or_review(title_id, review_id=None):
    """Получить объект Title или Review по идентификаторам."""
    title = get_object_or_404(Title, id=title_id)
    if review_id:
        return get_object_or_404(Review, id=review_id, title=title)
    return title
