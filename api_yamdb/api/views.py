from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Title

from .permissions import AdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class ListDeleteCreateViewSet(mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    pass


class GenreViewSet(ListDeleteCreateViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class CategoryViewSet(ListDeleteCreateViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [AdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
