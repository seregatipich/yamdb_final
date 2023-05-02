from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .permissions import IsAdmin, PermissionForReviewComment, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleGetSerializer, UserCreateSerializer,
                          UserSerializer)


@api_view(['POST'])
def create_user(request):
    """
    Обеспечивает функционал при работе с эндпоинтом /signup.
    Создается пользователь в БД.
    На почту отправляется письмо с кодом подтверждения.
    """
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user = User.objects.create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    User.objects.filter(username=username).update(
        confirmation_code=confirmation_code)
    send_mail(
        subject='Регистрация в YaMDB',
        message=f'Ваш код для подтверждения - {confirmation_code}',
        from_email='test@yandex.com',
        recipient_list=(request.data['email'],)
    )
    return Response(serializer.data)


@api_view(['POST'])
def create_token(request):
    """
    Обеспечивает функционал при работе с эндпоинтом /token.
    Генерируется jwt-токен.
    """
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    if not username or not confirmation_code:
        return Response(
            'Отсутствует обязательное поле или оно некорректно',
            status=status.HTTP_400_BAD_REQUEST
        )
    if not User.objects.filter(username=username).exists():
        return Response(
            'Имя пользователя неверное',
            status=status.HTTP_404_NOT_FOUND
        )
    user = User.objects.get(username=username)
    if user.confirmation_code == confirmation_code:
        token = AccessToken.for_user(user)
        return Response(
            {
                'access': str(token)
            }
        )
    return Response('Код подтверждения неверен',
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Объединяет логику для набора связанных представлений модели User.
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated & IsAdmin, )
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(IsAuthenticated, )
    )
    def me_profile(self, request, pk=None):
        """
        Обеспечивает функционал при работе с эндпоинтом /me.
        """
        username = request.user.username
        user = User.objects.get(username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                user, data=request.data,
                partial=True,
                context={'request': request}
            )
            if serializer.is_valid(raise_exception=True):
                if serializer.validated_data.get('role'):
                    serializer.validated_data['role'] = request.user.role
                serializer.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin,
                      mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Объединяет логику для набора связанных представлений модели Category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = ('slug')
    permission_classes = (IsAuthenticated & IsAdmin | ReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class GenreViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin,
                   mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Объединяет логику для набора связанных представлений модели Genre.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = ('slug')
    permission_classes = (IsAuthenticated & IsAdmin | ReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Объединяет логику для набора связанных представлений модели Title.
    """
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAuthenticated & IsAdmin | ReadOnly, )

    def get_serializer_class(self):
        return TitleGetSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Объединяет логику для набора связанных представлений модели Review.
    """
    serializer_class = ReviewSerializer
    permission_classes = (PermissionForReviewComment, )

    def get_queryset(self):
        """Формирует queryset из отзывов n-ого произведения."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return Review.objects.filter(title=title.id)

    def perform_create(self, serializer):
        """Создает отзыв с задаными полями: author, title."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Объединяет логику для набора связанных представлений модели Comment.
    """
    permission_classes = (PermissionForReviewComment, )
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Формирует queryset из комменатриев n-ого отзыва."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return Comment.objects.filter(review=review.id)

    def perform_create(self, serializer):
        """Создает комментарий с задаными полями: author, review."""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
