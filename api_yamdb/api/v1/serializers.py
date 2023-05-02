from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

START_SCORE = 1
END_SCORE = 10


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Преобразует информацию для работы через API по модели User.
    Используется при самостоятельной регистрации.
    """
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя не может быть "me"'
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    """
    Преобразует информацию для работы через API по модели User.
    Используется администратором для регистрации.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class GenreSerializer(serializers.ModelSerializer):
    """
    Преобразует информацию для работы через API по модели Genre.
    """
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """
    Преобразует информацию для работы через API по модели Category.
    """
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitlePostSerializer(serializers.ModelSerializer):
    """
    Преобразует информацию для работы через API по модели Title.
    Сериалайзер используется при POST запросах.
    """
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleGetSerializer(serializers.ModelSerializer):
    """
    Преобразует информацию для работы через API по модели Title.
    Сериалайзер используется при GET запросах.
    """
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        if obj.reviews.all().exists():
            return int(obj.reviews.aggregate(Avg('score'))['score__avg'])
        return None


class ValueTitleDefault(serializers.CurrentUserDefault):
    """
    Позволяет получить значение title из контекста.
    Для реализации проверки уникальности полей в Review.
    """
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context.get('view').kwargs.get('title_id')

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ReviewSerializer(serializers.ModelSerializer):
    """
    Преобразует информацию для работы через API по модели Review.
    """
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=ValueTitleDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='На это произведение можно оставлять только 1 отзыв!'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """
    Преобразует информацию для работы через API по модели Comment.
    """
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
