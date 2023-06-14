import datetime


def get_week_number(year: int, month: int, day: int) -> int:
    date = datetime.date(year, month, day)
    # week_number = date.isocalendar().week
    week_number = int(date.strftime("%U"))+1
    return week_number


def get_current_week_number() -> int:
    today = datetime.date.today()

    return get_week_number(today.year, today.month, today.day)


if __name__ == "__main__":
    print(get_week_number(2000, 1, 1))
    get_current_week_number()

    print(datetime.date(2000, 1, 1).strftime("%U"))


