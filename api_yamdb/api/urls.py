from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUpView, GetTokenView

router = DefaultRouter()
router.register(r'auth/signup', SignUpView)
router.register(r'auth/token', GetTokenView)
urlpatterns = [
    path('v1/', include(router.urls)),
]
