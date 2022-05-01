from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, GetTokenView, SignUpViewSet,
                    TitleViewSet, CommentViewSet, ReviewViewSet, UsersViewSet)

router = DefaultRouter()
router.register(r'auth/signup', SignUpViewSet, basename='signup')
router.register(r'users', UsersViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')
router.register(
    r'title/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='Review'
)
router.register(
    r'title/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='Comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', GetTokenView.as_view())
]
