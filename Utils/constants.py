sftp_door_close_forecast_time = '50'
lot_to_mwh = 10

'Power Plant\nUnit Price\nAfter GIP\n$/MWh'

report_cols = ['Date',
               'org',
               'Capacity\nMWh',
               'KGUP\nMWh',
               'KUDUP\nMWh',
               'UEVM\nMWh',
               'UEÇM\nMWh',
               'Intraday\nKUPST\nTL',
               'Day-Ahead\nKUPST\nTL',
               'TEİAŞ\nImproved\nAmount\nTL',
               'EPİAŞ\nImproved\nAmount\nTL',
               'KGUP Cost\n(w/o PIU)\nTL/MWh',
               'Imbalance\n Cost\nTL/MWh',
               'YEKDEM Unit\nPrice\n$/MWh',
               'Zero Imbalance\nUnit Price\n(with YEKBED)\n$/MWh',
               'Power Plant\nUnit Price\n(w/o GIP)\n$/MWh',
               'Power Plant\nUnit Price\n(with GIP)\n$/MWh',
               'Intraday\nMape',
               'Day-Ahead\nMape']

org_report_cols = ['Date',
                   'org',
                   'Capacity\nMWh',
                   'Day-Ahead\nMWh',
                   'Intraday\nMWh',
                   'UEVM\nMWh',
                   'UEÇM\nMWh',
                   'EPİAŞ\nImproved\nAmount\n$',
                   'Imbalance Cost\n(w/o PIU)\n$/MWh',
                   'KGUP Cost\n(w/o PIU)\nTL/MWh',
                   'Zero Imbalance\nUnit Price\n(with YEKBED)\n$/MWh',
                   'Organization\nUnit Price\n(w/o GIP)\n$/MWh',
                   'Organization\nUnit Price\nAfter GIP\n$/MWh',
                   'Organization\nUnit Price\nAfter Imb Sharing\n$/MWh',
                   'Intraday\nKUPST\nTL',
                   'Day-Ahead\nKUPST\nTL',
                   'TEİAŞ\nImproved\nAmount\nTL',
                   'Intraday\nMape',
                   'Day-Ahead\nMape']

import pandas as pd
org_names = pd.Series(index=['WIND', 'HYDRO', 'SOLAR', 'GEO', 'BIO'], data=['A', 'AA', 'AA1', 'AA2', 'AA3'])
plant_tolerance = pd.Series(index=['WIND', 'HYDRO', 'SOLAR', 'GEO', 'BIO', 'Portfolio'], data=['73', '73', '133', '133', '133', '73'])
