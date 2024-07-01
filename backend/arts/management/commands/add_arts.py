import csv
from collections import defaultdict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from arts.models import Art, Author, Category, Color, Orientation, Size, Style


User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        cache = defaultdict(dict)
        file_path = settings.BASE_DIR / "data/Arts.csv"
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(
                email="test@fake.com",
                first_name="test",
                last_name="test",
                phone_number="+79012345678",
            )

        def get_object(value, key, model, lookup_field):
            if value not in cache[key]:
                cache[key][value] = model.objects.get_or_create(
                    **{lookup_field: value}
                )[0]
            return cache[key][value]

        with open(file_path, "r", encoding="utf-8") as f:
            f.readline()
            for row in csv.reader(f):
                (
                    title,
                    _,
                    price,
                    category_name,
                    orientation_type,
                    style_name,
                    color_type,
                    size_name,
                    author_name,
                    year,
                    popular,
                ) = row
                if not title:
                    continue

                if author_name not in cache["author"]:
                    cache["author"][author_name] = Author.objects.get(
                        name=author_name
                    )
                author = cache["author"][author_name]
                try:
                    price = int(price.replace(r" ", "").replace(" ", ""))
                except ValueError:
                    self.stdout.write(
                        self.style.ERROR(f"Can't parse price - {price}")
                    )
                    continue

                category = get_object(
                    category_name, "category", Category, "name"
                )
                orientation = get_object(
                    orientation_type, "orientation", Orientation, "type"
                )
                style = get_object(style_name, "style", Style, "name")
                color = get_object(color_type, "color", Color, "type")
                size = get_object(size_name, "size", Size, "name")
                art, _ = Art.objects.get_or_create(
                    user=user,
                    title=title,
                    price=price,
                    category=category,
                    author=author,
                    orientation=orientation,
                    style=style,
                    color=color,
                    size=size,
                    year=year,
                    popular=popular,
                )
            self.stdout.write(self.style.SUCCESS("Added art objects"))
