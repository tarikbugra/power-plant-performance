import os
import datetime
import pandas as pd
from Utils import paths


def append_and_save(df, path):
    """

    Parameters
    ----------
    df: the data which is extracted from ftp

    Returns
    -------

    """
    if not os.path.exists(path):
        df.to_excel(path, index=True)
        output_df = df
    else:
        output_df = pd.read_excel(path, index_col=0)
        output_df.index = output_df.index.round(freq='s')
        output_df = output_df.append(df, sort=False)
        output_df = output_df.loc[~output_df.index.duplicated(keep='last')].sort_index()
        output_df.to_excel(path, index=True)

    return output_df
