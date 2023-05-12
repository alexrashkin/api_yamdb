from django.urls import include, path

from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, APIGetToken, APISignup, UsersViewSet

app_name = 'api'

router = DefaultRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router.urls)),
]

router = routers.SimpleRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
