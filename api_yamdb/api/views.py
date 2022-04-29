from django import views
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from requests import Response
from rest_framework import mixins, viewsets, views, status

from rest_framework_simplejwt.tokens import SlidingToken

from .serializers import UserSerializer, TokenSerializer

User = get_user_model()


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class SignUpView(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Код подтверждения',
            f'Ваш код: {confirmation_code}',
            'signup@yamdb.com',
            [user.email, ]
        )


class GetTokenView(views.APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']
            ):
                token = SlidingToken.for_user(user)
                user_data = [
                    {
                        "username": user.username,
                        "token": token
                    }
                ]
                serializer = TokenSerializer(user_data)
                return Response(
                    serializer.data,
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
