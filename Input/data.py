import pandas as pd
from Utils import paths, constants
from Connector.dbConnector import DatabaseConnector


class Data:
    def __init__(self):
        self.da = pd.DataFrame()
        self.da_plant_wise = None
        self.production_org_wise = pd.DataFrame()
        self.consumption_org_wise = pd.DataFrame()
        self.gip = pd.DataFrame()
        self.production = pd.DataFrame()
        self.kudup = pd.DataFrame()
        self.consumption = pd.DataFrame()
        self.ptf_smf = pd.read_excel(paths.mcp_smp_path, index_col=0)
        self.currency = pd.read_excel(paths.currency_path, index_col=0)
        self.installed_capacity = pd.read_excel(paths.eak_path, sheet_name='EAK_plant', index_col=0)

    def read_files(self):
        self.da = pd.read_excel(paths.gop_org_total, index_col=0)
        self.gip = pd.read_excel(paths.gip_org_total, index_col=0)
        self.production = pd.read_excel(paths.prod_org_total, index_col=0)
        self.kudup = pd.read_excel(paths.kudup_path, sheet_name='KUDUP_plant', index_col=0)
        self.consumption = pd.DataFrame(data=0, columns=self.production.columns, index=self.production.index)

    def process_data(self, date, get_from_daily_data=True):
        """

        :param date:
        :param dam_multiple_plants:
        :param get_from_daily_data:
        :return:
        """
        config = date.config
        self.installed_capacity = self.installed_capacity.rolling(48).max().bfill()

        if get_from_daily_data:
            self.read_files()
        else:
            self.get_settlement_data(date)

        self.gip.index = self.gip.index.round(freq='s')
        self.ptf_smf.index = self.ptf_smf.index.round(freq='s')
        self.set_org_wise_data(config, self.production, self.production_org_wise)
        self.set_org_wise_data(config, self.consumption, self.consumption_org_wise)

        self.da = self._fill_info(config, self.da, pd.DataFrame(), date.config.org_name, date.mtd_date_range)
        self.gip = self._fill_info(config, self.gip, pd.DataFrame(), date.config.org_name, date.mtd_date_range)
        self.production = self._fill_info(config, self.production, pd.DataFrame(), date.config.pp_name, date.mtd_date_range)
        self.consumption = self._fill_info(config, self.consumption, pd.DataFrame(), date.config.pp_name,
                                           date.mtd_date_range)

        self.production_org_wise = self._fill_info(config, self.production_org_wise, pd.DataFrame(),
                                                   date.config.pp_name, date.mtd_date_range)
        self.consumption_org_wise = self._fill_info(config, self.consumption_org_wise, pd.DataFrame(),
                                                    date.config.pp_name, date.mtd_date_range)
        self.kudup = self._fill_info(config, self.kudup, pd.DataFrame(), date.config.pp_name, date.mtd_date_range)
        self.installed_capacity = self._fill_info(config, self.installed_capacity, pd.DataFrame(),
                                                  date.config.pp_name, date.mtd_date_range)

        self.ptf_smf = self.ptf_smf.reindex(date.mtd_date_range).fillna(0)
        self.currency = self.currency.reindex(date.mtd_date_range).ffill()['TP_DK_USD_A_YTL']

        self.da_plant_wise = self.da.copy()
        dam_plant_wise = pd.read_excel(paths.pp_basis_path, index_col=0)
        dam_plant_wise.index = dam_plant_wise.index.round(freq='s')
        self.da_plant_wise.update(dam_plant_wise)

    @staticmethod
    def set_org_wise_data(config, data, self_data, name='pp_name'):
        unique_org_names = config['org_name'].unique()
        for org in unique_org_names:
            plant_names = config[config['org_name'] == org][name].to_list()
            for p_name in plant_names:
                self_data[p_name] = data[plant_names].sum(axis=1)

    @staticmethod
    def set_org_wise_truth_data(config, data, self_data, name='pp_name'):
        unique_org_names = config['org_name'].unique()
        for org in unique_org_names:
            plant_names = config[config['org_name'] == org][name].to_list()
            for p_name in plant_names:
                self_data[p_name] = data[plant_names].any(axis=1)

    def _add_group_info(self, config):
        """

        :return:
        """

        config_type = config.type.unique()
        org_name = config.set_index('org_name')['type'].to_dict()
        plant_type_pp_name = config.set_index('pp_name')['type'].to_dict()

        da = self.find_grouped_value(org_name, config_type, self.da)
        gip = self.find_grouped_value(org_name,  config_type, self.gip)
        production = self.find_grouped_value(plant_type_pp_name, config_type, self.production)
        consumption = self.find_grouped_value(plant_type_pp_name, config_type, self.consumption)
        production_org = self.find_grouped_value(plant_type_pp_name, config_type, self.production_org_wise)
        consumption_org = self.find_grouped_value(plant_type_pp_name, config_type, self.consumption_org_wise)
        kudup = self.find_grouped_value(plant_type_pp_name, config_type, self.kudup)
        installed_capacity = self.find_grouped_value(plant_type_pp_name, config_type, self.installed_capacity)
        out = [self._add_portfolio(i) for i in [da, gip, production, production_org, consumption, consumption_org, kudup, installed_capacity]]
        return out


    @staticmethod
    def _add_portfolio(data):
        """
        adding 'Portfolio' column to data, where the value is sum of all values in data
        :param data:
        :return:
        """
        data['Portfolio'] = data.sum(axis=1)
        return data

    @staticmethod
    def find_grouped_value(new_column_names, config_type, data):
        """
        Getting org_df and sums the values for each plant_type return new df
        :param new_column_names: Columns we considered
        :param config_type: WIND, SOLAR, GEO, BIO, HYDRO
        :param org_df: Data we are going to sum
        :return:
        """
        df_out = pd.DataFrame()
        df = data[list(new_column_names.keys())]
        df.rename(columns=new_column_names, inplace=True)

        for type in config_type:
            df_out[type] = df[type].sum(axis=1)
        return df_out

    @staticmethod
    def _fill_info(config, data, data_group, name, mtd_date_range):
        """

        :param data:
        :param data_group: data_group we are going to append
        :param name: Name of columns we are going to get from data
        :param mtd_date_range:
        :return:
        """
        filtered_data = data[name]
        filtered_data.columns = config['report_name']
        concat_data = pd.concat([data_group, filtered_data], axis=1)
        return concat_data.reindex(mtd_date_range).fillna(0)



