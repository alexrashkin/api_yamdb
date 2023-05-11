from django.urls import include, path
from rest_framework import routers

from api.views import ReviewViewSet, CommentViewSet

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
