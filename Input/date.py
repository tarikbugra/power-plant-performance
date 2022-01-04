import pandas as pd
import datetime
from Utils import paths


class Date:
    def __init__(self, day):
        self.first_date_of_month = datetime.date(day.year, day.month, 1)
        self.month = day.strftime('%Y-%m')
        self.year = day.strftime('%Y')
        self.month_for_path = self.month.replace('-', '/')
        self.month_for_settlement = day.strftime('%Y%m')
        self.day_str = day.strftime('%Y-%m-%d')
        self.day_str_currency = day.strftime('%d-%m-%Y')
        self.day_range = pd.date_range(start=self.day_str, freq='H', periods=24)
        self.mtd_date_range = pd.date_range(start=self.first_date_of_month, end=self.day_range[-1], freq='H')

        self.next_month = (day + datetime.timedelta(days=31)).strftime('%Y-%m')

        paths.prepare_paths(self)
        self.config = pd.read_excel(paths.config)
