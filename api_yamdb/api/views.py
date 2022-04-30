from django import views
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import mixins, viewsets, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import SlidingToken

from .serializers import UserSerializer, TokenSerializer
from .tokens import account_activation_token

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
            try:
                user = get_object_or_404(User, username=username)
            except Http404:
                return Response(
                    'Пользователя с таким username не существует',
                    status=status.HTTP_404_NOT_FOUND
                )
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
