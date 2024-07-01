import re
from datetime import date

from celery import shared_task
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Appraisal, Art
from .Paintings_v2 import ArtObject, predict
from .utils import get_age

DIGITS = r"\d+"


@shared_task
def get_appraisal_price(art_id: int, user_id) -> int:
    appraisal_obj = Appraisal.objects.filter(
        art_id=art_id, user_id=user_id
    ).select_related("author", "art")
    if appraisal_obj.exists():
        if appraisal_obj.first().status != Appraisal.Status.not_started:
            return -1
        else:
            appraisal_obj = appraisal_obj.first()
    else:
        appraisal_obj = Appraisal.objects.create(
            art_id=art_id,
            user_id=user_id,
            status=Appraisal.Status.in_progress,
        )

    art_object = appraisal_obj.art
    author = art_object.author

    age = get_age(author.birth_date, author.death_date)
    if age < 0:
        return -1

    match = re.findall(DIGITS, art_object.size.name)
    if not match or len(match) < 2:
        return -1

    height, width = map(float, match[:2])
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
        art_object.appraisal_price = int(predict(data))
        appraisal_obj.status = Appraisal.Status.completed
        appraisal_obj.save()
        art_object.save()

        return art_object.appraisal_price
