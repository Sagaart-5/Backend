import re
from datetime import date

from celery import shared_task
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Appraisal, Art
from .Paintings_v2 import ArtObject, predict


@shared_task
def get_appraisal_price(art_id: int, user_id) -> int:
    appraisal_obj = Appraisal.objects.filter(art_id=art_id, user_id=user_id)
    print(appraisal_obj)
    if (
        appraisal_obj.exists()
        and appraisal_obj.first().status != Appraisal.Status.not_started
    ):
        return -1
    else:
        appraisal_obj = Appraisal.objects.create(
            art_id=art_id, user_id=user_id
        )

    art_object = get_object_or_404(Art, id=art_id)
    size = art_object.size.name
    pattern = r"\d+"
    match = re.findall(pattern, size)
    if not match or len(match) < 2:
        return -1

    height, width = map(float, match[:2])
    author = art_object.author

    end_date = (
        author.death_date if author.death_date else timezone.now().date()
    )
    age = end_date.year - author.birth_date.year
    _end_date_some_year = date(
        day=end_date.day, month=end_date.month, year=author.birth_date.year
    )
    if author.birth_date > _end_date_some_year:
        age -= 1
    data = ArtObject(
        category=art_object.category.name,
        year=art_object.year,
        height=height,
        width=width,
        work_material="",
        pad_material="",
        country=author.country,
        sex=author.gender,
        solo_shows="музей",
        group_shows="музей",
        age=age,
    )
    with transaction.atomic():
        appraisal_obj.status = Appraisal.Status.completed
        appraisal_obj.save()
        art_object.appraisal_price = int(predict(data))
        art_object.save()

        return art_object.appraisal_price
