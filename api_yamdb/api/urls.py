from django.urls import include, path
from rest_framework import routers
from .views import APIGetToken, APISignup, UsersViewSet

app_name = 'api'

router = routers.SimpleRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
