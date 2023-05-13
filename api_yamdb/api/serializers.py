from rest_framework import serializers
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Review, Comment
from reviews.validators import validate_year
from users.models import User


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


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username')
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    # def validate(self, attr):
        # author = self.context["request"].user
        # if Review.objects.filter(
        #     title=value,
        #     author=author
        # ).exists():
        #     raise serializers.ValidationError("Можно оставлять только один отзыв")
        # return value

    def validate(self, attrs):
        title_id = self.context.get("view").kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        author = self.context["request"].user
        if self.context["request"].method == 'POST' and Review.objects.filter(
            title=title,
            author=author
        ).exists():
            raise serializers.ValidationError(
                "Можно оставлять только один отзыв")
        return attrs
    # def validate(self, value):
    #     if Review.objects.filter(
    #         title=self.context.get("view").kwargs.get("title_id"),
    #         author=self.context["request"].user
    #     ).exists():
    #         return value
    #     raise serializers.ValidationError("Можно оставлять только один отзыв")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username')
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
