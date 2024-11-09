import csv
import os
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

CSV_DIR = os.path.join(settings.BASE_DIR, 'static', 'data')


class Command(BaseCommand):
    help = 'Fills the database with data from csv-file in static folder'

    def handle(self, *args, **kwargs):
        FILE_HANDLE = (
            ('category.csv', Category, {}),
            ('genre.csv', Genre, {}),
            ('users.csv', User, {}),
            ('titles.csv', Title, {'category': 'category_id'}),
            ('genre_title.csv', Title.genre.through, {}),
            ('review.csv', Review, {'author': 'author_id'}),
            ('comments.csv', Comment, {'author': 'author_id'}),
        )

        for file, model, replace in FILE_HANDLE:
            self.stdout.write(f'Начинаем импорт из файла {file}')
            with open(Path(CSV_DIR, file), mode='r', encoding='utf8') as f:
                reader = csv.DictReader(f)
                counter = 0
                failed_entries = 0
                for row in reader:
                    counter += 1
                    args = dict(**row)
                    if replace:
                        for old, new in replace.items():
                            args[new] = args.pop(old)
                    try:
                        model.objects.create(**args)
                    except Exception as e:
                        self.stdout.write(
                            f'Ошибка при импорте строки {counter}: {e}'
                        )
                        failed_entries += 1

                self.stdout.write(
                    f'Обработано строк: {counter}; '
                    f'Добавлено объектов: {counter - failed_entries}; '
                    f'Ошибок при импорте: {failed_entries}')
