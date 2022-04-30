from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, GetTokenView, SignUpView,
                    TitleViewSet)

router = DefaultRouter()
router.register(r'auth/signup', SignUpView, basename='signup')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', GetTokenView.as_view())
]
