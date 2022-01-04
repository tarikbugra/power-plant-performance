import pandas as pd
import datetime
from DataFetcher import epias_transparency
from Utils import utils
from Utils import paths


def get_mcp_smp(s_date, e_date):
    mcp_smp = epias_transparency.get_mcp_smp(s_date, e_date)
    mcp_smp['date'] = pd.to_datetime(mcp_smp['date'].str[0:-5], format='%Y-%m-%dT%H:%M:%S.%f')
    mcp_smp.set_index('date', inplace=True)
    mcp_smp.index = mcp_smp.index.round(freq='s')

    return utils.append_and_save(mcp_smp, paths.mcp_smp_path)


def get_dam_data():
    dam = pd.read_excel(paths.multiple_dam_path, index_col=0, sheet_name='For KUPST New')
    dam.index = dam.index.round(freq='s')
    dam = dam.dropna(axis=0)
    return utils.append_and_save(dam, paths.pp_basis_path)





