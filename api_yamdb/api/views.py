from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from reviews.models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review=self.get_review_id())

    def get_review_id(self):
        return self.kwargs.get("review_id")

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.get_review_id())
        serializer.save(review=review, author=self.request.user)
