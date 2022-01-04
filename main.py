import datetime
from AllunitPrice import KupstPriceCalculator
from Input.data import Data
from excel_creator import app
from DataFetcher import epias_fetcher
from DataFetcher import currency_fetcher
from Input.date import Date
from Connector import smtp_connector


def prepare_input_data(date, use_new_daily_data=True, get_daily_Data=True):
    if get_daily_Data:
        # Fetch mcp_smp
        epias_fetcher.get_mcp_smp(date.day_str, date.day_str)
        epias_fetcher.get_dam_data()
        currency_fetcher.get_currency(date.day_str_currency, date.day_str_currency, date.month)
    data = Data()
    data.process_data(date, use_new_daily_data)
    return data


def run(date, without_settlement_run, get_daily_data):
    data = prepare_input_data(date, without_settlement_run, get_daily_data)
    cUP = KupstPriceCalculator(date)
    cUP.run(data)


if __name__ == '__main__':
    debug = False

    if not debug:
        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
        d = Date(yesterday)

        if yesterday.day == 20:
            # run settlement
            last_month_last_day = d.first_date_of_month - datetime.timedelta(days=1)
            run(Date(last_month_last_day), without_settlement_run=False, get_daily_data=True)

        run(d, without_settlement_run=True, get_daily_data=True)
        app(d, d.config)
        app(d, d.config, 'Organizations', 'org-')
        smtp_connector.send_email('', '', '', 'KUPST and Unit Price', d)
    else:
        use_settlement = True
        day = '2021-02-28'
        d = Date(datetime.datetime.strptime(day, '%Y-%m-%d'))
        run(d, without_settlement_run=not use_settlement, get_daily_data=False)
