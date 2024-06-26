import csv
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.utils import timezone

from arts.models import Author, Art, Category, Orientation, Style, Color, Size


User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / "data/Arts.csv"
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(
                email="test@fake.com",
                first_name="test",
                last_name="test",
                phone_number="+79012345678",
            )

        with open(file_path, "r", encoding="utf-8") as f:
            header = f.readline()
            for row in csv.reader(f):
                (
                    title,
                    _,
                    price,
                    category,
                    orientation,
                    style,
                    color,
                    size,
                    author_name,
                ) = row
                if not title:
                    continue

                art_author, _ = Author.objects.get_or_create(name=author_name)
                category, _ = Category.objects.get_or_create(name=category)
                price = int(price.replace(r" ", "").replace(" ", ""))
                orientation, _ = Orientation.objects.get_or_create(
                    type=orientation
                )
                style, _ = Style.objects.get_or_create(name=style)
                color, _ = Color.objects.get_or_create(type=color)
                size, _ = Size.objects.get_or_create(name=size)
                Art.objects.get_or_create(
                    author=user,
                    title=title,
                    price=price,
                    category=category,
                    art_author=art_author,
                    orientation=orientation,
                    style=style,
                    color=color,
                    size=size,
                    year=timezone.now().year - random.randint(15, 150),
                )
            self.stdout.write(self.style.SUCCESS(f"Added art objects"))
