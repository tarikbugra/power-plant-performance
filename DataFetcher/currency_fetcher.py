import requests
import datetime
import pandas as pd
from Utils import utils
from Utils import paths


def get_currency(startDate, endDate, month_):
    """
    Extract foreign exchange with the Central Bank's web service
    """

    url = f'https://evds2.tcmb.gov.tr/service/evds/series=TP.DK.USD.A.YTL&startDate={startDate}&endDate={endDate}' + \
          '&type=json&key='

    response = requests.get(url)
    json_data = response.json()['items']
    currency_ = pd.DataFrame(json_data)
    currency_['Tarih'] = pd.to_datetime(currency_['Tarih'], format='%d-%m-%Y')
    currency_ = currency_.drop(columns=['UNIXTIME']).set_index('Tarih')
    #paths.prepare_paths(month_)
    return utils.append_and_save(currency_, paths.currency_path)




