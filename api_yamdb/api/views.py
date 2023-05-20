from api.permissions import AdminOnly, AuthorAdminModeratorOrReadOnly
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import (MethodNotAllowed, PermissionDenied,
                                       ValidationError)
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          NotAdminSerializer, ReviewSerializer,
                          SignUpSerializer, TitleCreateSerializer,
                          TitleGetSerializer, UsersSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
           request.user.role in ['user', 'moderator']:
            raise PermissionDenied("Недостаточно прав для создания категории")
        elif not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug')
        if slug is not None:
            queryset = queryset.filter(slug=slug)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif request.user.role in ['user', 'moderator']:
            raise PermissionDenied("Недостаточно прав для изменения категории")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'user':
            raise PermissionDenied("Недостаточно прав для удаления категории")
        if request.user.is_authenticated and request.user.role == 'moderator':
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'detail': 'Недостаточно прав для удаления категории'}
            )
        elif not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        category = self.get_object()
        if category.titles.exists():
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'detail': 'Эта категория содержит связанные объекты'})
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug')
        if slug is not None:
            queryset = queryset.filter(slug=slug)
        return queryset

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
           request.user.role in ['user', 'moderator']:
            raise PermissionDenied("Недостаточно прав для создания жанра")
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            if self.kwargs.get('slug') is None:
                raise Http404
            raise MethodNotAllowed(request.method)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def partial_update(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
           request.user.role in ['user', 'moderator']:
            raise PermissionDenied("Недостаточно прав для изменения жанра")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
           request.user.role in ['user', 'moderator']:
            raise PermissionDenied("Недостаточно прав для удаления жанра.")
        return super().destroy(request, *args, **kwargs)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""

    queryset = Title.objects.all()
    serializer_class = TitleGetSerializer
    filterset_class = TitleFilter
    search_fields = ('name',)
    ordering = ('name',)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TitleCreateSerializer
        return TitleGetSerializer

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
           request.user.role in ['user', 'moderator']:
            raise PermissionDenied(
                "Недостаточно прав для создания произведения"
            )
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            raise MethodNotAllowed(request.method)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    def partial_update(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
           request.user.role in ['user', 'moderator']:
            raise PermissionDenied(
                "Недостаточно прав для изменения произведения"
            )

        name = request.data.get('name')
        if name and len(name) > 256:
            raise ValidationError(
                "Название произведения не может быть длиннее 256 символов"
            )

        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
           request.user.role in ['user', 'moderator']:
            raise PermissionDenied(
                "Недостаточно прав для удаления произведения"
            )
        return super().destroy(request, *args, **kwargs)


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    http_method_names = ('get', 'post', 'patch', 'delete', )

    @action(
        methods=('GET', 'PATCH'),
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIGetToken(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.

    Права доступа: Доступно без токена.

    Пример тела запроса:
    {
        "username": "string",
        "confirmation_code": "string"
    }
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    """
    Получить код подтверждения на переданный email.

    Права доступа: Доступно без токена.
    Использовать имя 'me' в качестве username запрещено.
    Поля email и username должны быть уникальными.

    Пример тела запроса:
    {
        "email": "string",
        "username": "string"
    }.
    """

    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        try:
            user, created = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError:
            return Response('Пользователи с таким username'
                            'или email уже существуют',
                            status=status.HTTP_400_BAD_REQUEST)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения.',
            message=f'Здравствуйте, {user.username}.'
                    f'\nКод подтверждения для доступа: {confirmation_code}',
            from_email=None,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def get_title_id(self):
        return self.kwargs.get("title_id")

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title_id())

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.get_title_id())
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (AuthorAdminModeratorOrReadOnly,)

    def get_review_id(self):
        return self.kwargs.get("review_id")

    def get_queryset(self):
        return Comment.objects.filter(review=self.get_review_id())

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.get_review_id())
        serializer.save(review=review, author=self.request.user)
