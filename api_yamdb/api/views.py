from django.shortcuts import render
from rest_framework import filters, viewsets
from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, Genre, Title

from .filters import TitleFilter
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleCreateSerializer, TitleGetSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """ Вьюсет для работы с произведениями """
    queryset = Title.objects.all()
    serializer_class = TitleGetSerializer
    filterset_class = (TitleFilter,)
    search_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return TitleCreateSerializer
        return TitleGetSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """ Вьюсет для работы с категориями """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    """ Вьюсет для работы с жанрами """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)