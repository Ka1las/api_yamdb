from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUpView, GetTokenView, CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register(r'auth/signup', SignUpView, basename='signup')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', GetTokenView.as_view())
]
