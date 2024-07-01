from datetime import date
from unittest import TestCase

from .utils import get_age


class TestAge(TestCase):
    def test_age(self):
        birth_date = date(1975, 3, 12)
        for end_date, expected_age in (
            (date(2020, 1, 1), 44),
            (date(2020, 12, 31), 45),
            (None, 49),
            (date(1939, 3, 5), -1)
        ):
            with self.subTest(end_date=end_date):
                self.assertEqual(get_age(birth_date, end_date), expected_age)
