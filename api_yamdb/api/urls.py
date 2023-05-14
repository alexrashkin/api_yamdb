from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    APIGetToken, APISignup, UsersViewSet, CommentViewSet,
                    ReviewViewSet)

app_name = 'api'
api_version = 'v1'

router_v1 = DefaultRouter()

router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path(f'{api_version}/', include(router_v1.urls)),
    path(f'{api_version}/auth/token/',
         APIGetToken.as_view(),
         name='get_token'),
    path(f'{api_version}/auth/signup/', APISignup.as_view(), name='signup'),
]
