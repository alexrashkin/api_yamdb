from rest_framework import serializers
from reviews.models import Category, Genre, Title
from reviews.validators import validate_year


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        

class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True),
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = 'id', 'name', 'category', 'genre', 'year', 'description'


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    description = serializers.CharField(required=False)
    year = serializers.IntegerField(required=False, validators=[validate_year])

    class Meta:
        model = Title
        fields = 'id', 'name', 'category', 'genre', 'year', 'description'
    