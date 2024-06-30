import csv

from django.conf import settings
from django.core.management import BaseCommand

from arts.models import Author


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / "data/Artists.csv"

        with open(file_path, "r", encoding="utf-8") as f:
            f.readline()
            for name, description in csv.reader(f):
                Author.objects.update_or_create(
                    name=name, defaults={"description": description}
                )
            self.stdout.write(self.style.SUCCESS("Successfully added Artists"))
