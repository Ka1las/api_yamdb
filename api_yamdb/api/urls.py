from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUpView, GetTokenView

router = DefaultRouter()
router.register(r'auth/signup', SignUpView, basename='signup')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', GetTokenView.as_view())
]
