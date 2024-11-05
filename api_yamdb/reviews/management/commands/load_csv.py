import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title
)
from users.models import MyUser


FILES_CLASSES = {
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': GenreTitle,
    'users.csv': MyUser,
    'review.csv': Review,
    'comments.csv': Comment,
}

COLUMN_MAPPINGS = {
    'users.csv': {
        'username': 'username', 'email': 'email',
        'role': 'role', 'bio': 'bio',
        'first_name': 'first_name', 'last_name': 'last_name'
    },
    'category.csv': {
        'name': 'name', 'slug': 'slug',
    },
    'genre.csv': {
        'name': 'name', 'slug': 'slug',
    },
    'titles.csv': {
        'name': 'name', 'year': 'year', 'category': 'category',
    },
    'genre_title.csv': {
        'title_id': 'title', 'genre_id': 'genre',
    },
    'review.csv': {
        'title_id': 'title', 'text': 'text',
        'author': 'author', 'score': 'score',
        'pub_date': 'pub_date',
    },
    'comments.csv': {
        'review_id': 'review', 'text': 'text',
        'author': 'author', 'pub_date': 'pub_date',
    },
}


class Command(BaseCommand):
    """Импортирует данные из csv-файлов в базу данных."""
    help: str = 'Импортирует данные из csv-файлов в базу данных'

    def handle(self, *args, **kwargs):
        directory = os.path.join(settings.BASE_DIR, 'static', 'data')

        if not os.path.isdir(directory):
            self.stdout.write(
                self.style.ERROR(f"Папка {directory} не найдена.")
                )
            return

        csv_files = [f for f in os.listdir(directory) if f in FILES_CLASSES]

        if not csv_files:
            self.stdout.write(
                self.style.WARNING(f"Нет CSV файлов в папке {directory}.")
                )
            return

        for csv_file in csv_files:
            csv_path = os.path.join(directory, csv_file)
            model = FILES_CLASSES[csv_file]
            column_mapping = COLUMN_MAPPINGS[csv_file]

            self.import_csv(csv_path, model, column_mapping)

    def import_csv(self, csv_path, model, column_mapping):
        with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data = self.filter_data(row, column_mapping)
                self.create_or_update_instance(model, data)

        self.stdout.write(
            self.style.SUCCESS(
                f"Данные из файла {os.path.basename(csv_path)} "
                "успешно загружены."
                )
            )

    def filter_data(self, row, column_mapping):
        return {
            field: row[column] for column, field in column_mapping.items()
            if column in row
            }

    def create_or_update_instance(self, model, data):
        instance, created = model.objects.get_or_create(**data)
        if not created:
            for field, value in data.items():
                setattr(instance, field, value)
            instance.save()
