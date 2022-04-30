from django import views
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import mixins, viewsets, views, status, filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import SlidingToken
from .serializers import UserSerializer, TokenSerializer, CategorySerializer, GenreSerializer, TitleSerializer
from .tokens import account_activation_token
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Title
from .permissions import AdminOrReadOnly


User = get_user_model()


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class SignUpView(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        confirmation_code = account_activation_token.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Ваш код: {confirmation_code}',
            'signup@yamdb.com',
            [user.email, ]
        )


class GetTokenView(views.APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = User.objects.get(username=username)
            if account_activation_token.check_token(
                user, serializer.validated_data['confirmation_code']
            ):
                token = str(SlidingToken.for_user(user))
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
