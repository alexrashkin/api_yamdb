from django.urls import include, path
from rest_framework import routers


from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from .views import (APIGetToken, APISignup, CategoryViewSet, GenreViewSet,
                    TitleViewSet, UsersViewSet, ReviewViewSet, CommentViewSet)

app_name = 'api'
api_version = 'v1'

router_v1 = routers.DefaultRouter()
router_v1.register('reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path(f'{api_version}/', include(router_v1.urls)),
]


app_name = 'api'

router = DefaultRouter()
router = routers.SimpleRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
