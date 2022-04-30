from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Avg
from reviews.models import Category, Genre, Title
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=150)

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise ValidationError(
                'Пользователь с таким username не существует!'
            )
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        rating = obj.score.all().aggregate(Avg('score')).get('score__avg')
        if rating is None:
            return 0
        return rating
