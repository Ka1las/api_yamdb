from django import views
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, permissions, status, views,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Review, Title

from .permissions import (AdminOrReadOnly, AuthorAdminModeratorPermission,
                          IsAdmin, IsSuperuser)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TokenSerializer, UserSignUpSerializer,
                          UserSerializer)
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg
from .tokens import account_confirmation_token

User = get_user_model()


class SignUpView(views.APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            confirmation_code = account_confirmation_token.make_token(user)
            send_mail(
                'Код подтверждения',
                f'Ваш код: {confirmation_code}',
                'signup@yamdb.com',
                [user.email, ]
            )
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class GetTokenView(views.APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = get_object_or_404(User, username=username)
            except Http404:
                return Response(
                    'Пользователя с таким username не существует',
                    status=status.HTTP_404_NOT_FOUND
                )
            if account_confirmation_token.check_token(
                user, serializer.validated_data['confirmation_code']
            ):
                token = str(AccessToken.for_user(user))
                user_data = {
                    "username": user.username,
                    "token": token
                }
                return Response(
                    user_data,
                    status=status.HTTP_200_OK
                )
            return Response(
                'Неверный код подтверждения',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin | IsSuperuser]
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    @action(
        methods=['get'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated, ]
    )
    def get_user(self, request):
        user = request.user
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)

    @get_user.mapping.patch
    def patch_user(self, request):
        user = request.user
        serializer = UserSerializer(user, request.data, partial=True)
        if serializer.is_valid():
            if user.role == user.USER:
                serializer.save(role=user.USER)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            'Ошибка в передаваемых данных',
            status=status.HTTP_400_BAD_REQUEST
        )


class ListDeleteCreateViewSet(mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    pass


class GenreViewSet(ListDeleteCreateViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly, )
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class CategoryViewSet(ListDeleteCreateViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly, )
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        AuthorAdminModeratorPermission,
        permissions.IsAuthenticatedOrReadOnly
    )  # Проверить

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        print(title.reviews.order_by('id'))
        return title.reviews.order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        AuthorAdminModeratorPermission,
        permissions.IsAuthenticatedOrReadOnly
    )  # Проверить

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
