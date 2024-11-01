from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from reviews.models import Title, Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import AnonimReadOnly, ReviewCommentPermissions


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AnonimReadOnly, ReviewCommentPermissions]

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
    permission_classes = [AnonimReadOnly, ReviewCommentPermissions]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
