from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APIGetToken, APISignup, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UsersViewSet)

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
    basename='comments'
)

urlpatterns = [
    path(f'{api_version}/', include(router_v1.urls)),
    path(f'{api_version}/auth/token/', APIGetToken.as_view(),
         name='get_token'),
    path(f'{api_version}/auth/signup/', APISignup.as_view(), name='signup'),
    path(
        f'{api_version}/genres/<slug:slug>/',
        GenreViewSet.as_view({'get': 'retrieve'}),
        name='genre_detail'
    ),
    path(
        f'{api_version}/titles/<int:title_id>/reviews/'
        f'<int:review_id>/comments/<int:pk>/',
        CommentViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
        name='comment_detail'
    ),
    path(
        f'{api_version}/titles/<int:title_id>/reviews/<int:pk>/',
        ReviewViewSet.as_view({'get': 'retrieve'}),
        name='review_detail'
    ),
    path(
        f'{api_version}/titles/<int:pk>/',
        TitleViewSet.as_view({'get': 'retrieve'}),
        name='title_detail'
    ),
    path(
        f'{api_version}/users/me/',
        UsersViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
        name='user_me'
    ),
    path(
        f'{api_version}/users/<int:pk>/',
        UsersViewSet.as_view({'get': 'retrieve'}),
        name='user_detail'
    ),
]
