from django.db import models


class Subscription(models.Model):
    duration = models.CharField(
        max_length=20,
        choices=[
            ('1 месяц', '1 месяц'),
            ('6 месяцев', '6 месяцев'),
            ('12 месяцев', '12 месяцев'),
        ],
        verbose_name='Длительность подписки'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.IntegerField(
        verbose_name='Цена'
    )
