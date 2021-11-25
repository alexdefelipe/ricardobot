from datetime import date, timedelta


class DateUtils:
    @staticmethod
    def get_last_friday() -> date:
        last_friday = date.today()

        while last_friday.isoweekday() != 5:
            last_friday -= timedelta(days=1)

        return last_friday

    @staticmethod
    def get_next_friday() -> date:
        next_friday = date.today()

        while next_friday.isoweekday() != 5:
            next_friday += timedelta(days=1)

        return next_friday
