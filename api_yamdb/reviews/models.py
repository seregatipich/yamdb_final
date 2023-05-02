from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from .validators import validate_custom_year


class AbstractModel(models.Model):
    """
    Абстракт. модель для создания жанра и категории.
    """
    name = models.TextField('Название', max_length=256)
    slug = models.SlugField('Сокращ. название',
                            unique=True, max_length=50)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(AbstractModel):
    """
    Модель для создания жанра.
    """

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(AbstractModel):
    """
    Модель для создания категории.
    """

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """
    Модель для создания произведения.
    """
    name = models.TextField('Название произведения', max_length=150)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    description = models.TextField(
        'Описание',
        max_length=1000,
        blank=True,
        null=True
    )
    year = models.PositiveSmallIntegerField(
        'Год', validators=[validate_custom_year])
    rating = models.PositiveSmallIntegerField(
        'Рэйтинг',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Модель для создания отзыва о произведении.
    """
    text = models.TextField('Текст отзыва', max_length=10000)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Модель для создания комментария к отзыву.
    """
    text = models.TextField('Текст комментария', max_length=1000)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
