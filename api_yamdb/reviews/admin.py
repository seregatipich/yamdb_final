from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)


class GenreInline(admin.TabularInline):
    model = Title.genre.through


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    inlines = [
        GenreInline,
    ]


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = [
        GenreInline,
    ]
    exclude = ('genre',)
