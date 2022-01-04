"""
Created on Thu Jul 18 14:41:55 2019

@author: Bugra
"""

import requests as req
import pandas as pd


def get_data_from_rest_service(url_tail, url_header, url='https://seffaflik.epias.com.tr/transparency/service/'):
    while True:
        try:
            resp = req.get(url + url_tail)
            data = resp.json()['body'][url_header]
            data = pd.DataFrame(data)
        except Exception as e:
            print('There is a problem' + str(e))
        else:
            break
    return data
