from datetime import date


def get_age(start_date: date, end_date: date | None) -> int:
    if end_date is not None and start_date >= end_date:
        return -1
    end_date = end_date if end_date else date.today()
    age = end_date.year - start_date.year
    end_date_same_year = date(
        day=end_date.day, month=end_date.month, year=start_date.year
    )
    if start_date > end_date_same_year:
        age -= 1
    return age
