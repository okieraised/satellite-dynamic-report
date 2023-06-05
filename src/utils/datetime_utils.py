import datetime


def get_week_number(year: int, month: int, day: int) -> int:
    date = datetime.date(year, month, day)
    week_number = date.isocalendar().week
    return week_number


def get_current_week_number() -> int:
    today = datetime.date.today()

    return get_week_number(today.year, today.month, today.day)


if __name__ == "__main__":
    get_week_number(2023, 6, 5)
    get_current_week_number()


