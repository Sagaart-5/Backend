import csv
from datetime import datetime

from django.conf import settings
from django.core.management import BaseCommand

from arts.models import Author


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / "data/Artists.csv"

        with open(file_path, "r", encoding="utf-8") as f:
            f.readline()
            for (
                name,
                description,
                gender,
                country,
                birth_date,
                death_date,
            ) in csv.reader(f):
                if death_date:
                    death_date = datetime.strptime(death_date, "%d.%m.%Y")
                else:
                    death_date = None
                Author.objects.update_or_create(
                    name=name,
                    description=description,
                    gender=gender[0],
                    country=country,
                    birth_date=datetime.strptime(birth_date, "%d.%m.%Y"),
                    death_date=death_date,
                )
            self.stdout.write(self.style.SUCCESS("Successfully added Artists"))
