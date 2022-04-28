from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets

from .permissions import # импортировать пермишин как создам
from .serializers import (CommentSerializer, ReviewSerializer)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = () # Разобраться с правами доступа и написать пермишины

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = () # Разобраться с правами доступа и написать пермишины

    def get_queryset(self):
        review = get_object_or_404(
            Review, 
            id=self.kwargs.get('review_id'), 
            title=self.kwargs.get('title_id'))
        return review.comments.order_by('id')

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, 
            id=self.kwargs.get('review_id'), 
            title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)

