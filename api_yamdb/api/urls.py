from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet

router = DefaultRouter()

router.register(
    r'title/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='Review'
)
router.register(
    r'title/(?P<title_id>[0-9]+)/reviews/(?P,review_id[0-9]+)/comments',
    CommentViewSet,
    basename='Comment'
)

urlpatterns = [
    path(
        'v1/api-token-auth/',
        views.obtain_auth_token,
        name='obtain_auth_token'
    ),
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),  # Сделал пока через джозер, позже сделаю токен самостоятельно.
]
