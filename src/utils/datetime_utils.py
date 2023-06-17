import datetime


def get_date_from_week_number(year: int, week: int) -> str:
    date_in_week = f'{year}-W{week-1}'
    r = datetime.datetime.strptime(date_in_week + '-1', '%G-W%V-%u').strftime('%Y-%m-%d')
    return r


def get_week_number(year: int, month: int, day: int) -> int:
    date = datetime.date(year, month, day)
    # week_number = date.isocalendar().week
    week_number = int(date.strftime("%U"))+1
    return week_number


def get_current_week_number() -> int:
    today = datetime.date.today()

    return get_week_number(today.year, today.month, today.day)


def validate_file_format(date_text: str):
    try:
        datetime.date.fromisoformat(date_text)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    print(get_week_number(2000, 1, 1))
    get_current_week_number()
    print(datetime.date(2000, 1, 1).strftime("%U"))
    get_date_from_week_number(2015, 6)


