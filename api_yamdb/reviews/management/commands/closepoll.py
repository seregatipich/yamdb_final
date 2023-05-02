import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

MODEL_FILE = {
    Genre: 'static/data/genre.csv',
    Category: 'static/data/category.csv',
    Title: 'static/data/titles.csv',
    User: 'static/data/users.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv'
}


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        for model, dir in MODEL_FILE.items():
            with open(dir, encoding='utf-8-sig') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                for row in reader:
                    model.objects.get_or_create(**row)
