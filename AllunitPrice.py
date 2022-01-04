import datetime
import pandas as pd
import numpy as np
from Utils import paths
from Utils import constants


class KupstPriceCalculator:
    def __init__(self, date):
        self.first_date_of_month = date.first_date_of_month
        self.last_day_date_range = date.day_range
        self.mtd_date_range = date.mtd_date_range
        self.month = date.month
        self.config = date.config.set_index('report_name')

    def run(self, data):
        df_plant = self.run_plant_wise(data)
        df_type = self.run_type_wise(data, df_plant)
        df_org = self.run_org_wise(data, df_plant)

    def run_plant_wise(self, data):
        gip_share = self.find_gip_share(data)

        dam_hourly_income = data.da_plant_wise.mul(data.ptf_smf['mcp'], axis=0).fillna(0)
        gip_hourly_income = gip_share.mul(data.ptf_smf['mcp'], axis=0).fillna(0)

        yekdem = self.config.yekdem_price
        dam_edt = self.calculate_hourly_imbalance_cost(data.production - data.da_plant_wise, data.ptf_smf)
        gip_edt = self.calculate_hourly_imbalance_cost(data.production - data.da_plant_wise-gip_share, data.ptf_smf)

        dam_net_hourly_income = dam_hourly_income + dam_edt
        gip_net_hourly_income = dam_hourly_income + gip_hourly_income + gip_edt

        hourly_zero_imbalance = data.production.mul(data.ptf_smf['mcp'], axis=0)
        hourly_zero_imbalance_dollar = data.production.mul(data.ptf_smf['mcp'], axis=0).divide(data.currency, axis=0)
        kupst = self.calculate_hourly_kupst(data.kudup, data)
        dam_kupst = self.calculate_hourly_kupst(data.da_plant_wise, data)

        df = pd.DataFrame()
        df['Capacity\nMWh'] = (data.installed_capacity.loc[self.last_day_date_range]).mean().round(1)
        df['KGUP\nMWh'] = data.da_plant_wise.sum().round(1)
        df['KUDUP\nMWh'] = data.kudup.sum().round(1)
        df['UEVM\nMWh'] = data.production.sum().round(1)
        df['UEÇM\nMWh'] = data.consumption.sum().round(1)
        df['EPİAŞ\nImproved\nAmount\nTL'] = (gip_net_hourly_income-dam_net_hourly_income).sum().round(0)

        df['KGUP Cost\n(w/o PIU)\nTL/MWh'] = -(kupst.sum()/data.production.sum()).round(2)
        df['Imbalance\n Cost\nTL/MWh'] =(
                    (gip_net_hourly_income - hourly_zero_imbalance).sum()/data.production.sum()).round(2)
        df['YEKDEM Unit\nPrice\n$/MWh'] = yekdem
        df['YEKBED \n$/MWh'] = yekdem - self.config.j_coefficient*(hourly_zero_imbalance_dollar.sum()/data.production.sum()).round(2)
        # YEKDEM price + (1-tolerance)*ptf/kur
        df['Zero Imbalance\nUnit Price\n(with YEKBED)\n$/MWh'] = (yekdem + \
            (1-self.config.j_coefficient)*(hourly_zero_imbalance_dollar.sum()/data.production.sum())).round(2)
        df['Power Plant\nUnit Price\n(w/o GIP)\n$/MWh'] = (df['YEKBED \n$/MWh'] +
                (dam_net_hourly_income.divide(data.currency, axis=0)).sum()/data.production.sum()).round(2)
        df['Power Plant\nUnit Price\n(with GIP)\n$/MWh'] = (df['YEKBED \n$/MWh'] + gip_net_hourly_income.divide(data.currency,axis=0).sum()/data.production.sum()).round(2)
        df['Intraday\nKUPST\nTL'] = kupst.sum().round()
        df['Day-Ahead\nKUPST\nTL'] = dam_kupst.sum().round()
        df['TEİAŞ\nImproved\nAmount\nTL'] = (dam_kupst.sum()-kupst.sum()).round()
        df['Intraday\nMape'] = (abs(data.production - data.kudup) / data.installed_capacity).mean().round(4)
        df['Day-Ahead\nMape'] = (abs(data.production - data.da_plant_wise) / data.installed_capacity).mean().round(4)
        df['Date'] = self.month
        df['org'] = self.config.org_name
        df.index.name = 'Power Plants'
        return df

    def run_org_wise(self, data, df_plant_wise):
        dam_hourly_income = data.da.mul(data.ptf_smf['mcp'], axis=0).fillna(0)
        gip_hourly_income = data.gip.mul(data.ptf_smf['mcp'], axis=0).fillna(0)

        dam_edt = self.calculate_hourly_imbalance_cost(data.production_org_wise - data.da, data.ptf_smf)
        gip_edt = self.calculate_hourly_imbalance_cost(data.production_org_wise - data.da - data.gip,
                                                       data.ptf_smf)
        edt_shared = self.calculate_edt_shared(data.production_org_wise, data.da, data.gip, data.ptf_smf)
        gip_net_hourly_income = (dam_hourly_income + gip_hourly_income + gip_edt).divide(data.currency, axis=0).sum()
        dam_net_hourly_income = (dam_hourly_income + dam_edt).divide(data.currency, axis=0).sum()
        hourly_zero_imbalance = data.production_org_wise.mul(data.ptf_smf['mcp'], axis=0).divide(data.currency, axis=0).sum()
        gip_net_hourly_income_edt_shared = (dam_hourly_income + gip_hourly_income + edt_shared).divide(data.currency, axis=0).sum()

        orgs = self.config['org_name'].unique()
        df = pd.DataFrame()

        for org in orgs:
            plants_under_org = self.config[self.config['org_name'] == org].index
            plant_wise_data = df_plant_wise.loc[plants_under_org, :]
            production = data.production[plants_under_org]
            total_prod = production.sum(axis=1).sum()
            yekbed = (plant_wise_data['YEKBED \n$/MWh'] * production.sum()).sum()
            df.loc[org, 'Capacity\nMWh'] = plant_wise_data['Capacity\nMWh'].sum()
            df.loc[org, 'Day-Ahead\nMWh'] = round(data.da[plants_under_org].sum().mean(), 1)
            df.loc[org, 'Intraday\nMWh'] = round(data.gip[plants_under_org].sum().mean(), 1)
            df.loc[org, 'UEVM\nMWh'] = total_prod.round(1)
            df.loc[org, 'UEÇM\nMWh'] = plant_wise_data['UEÇM\nMWh'].sum().round(1)
            df.loc[org, 'EPİAŞ\nImproved\nAmount\n$'] = round((gip_net_hourly_income-dam_net_hourly_income)[plants_under_org].mean(), 0)
            df.loc[org, 'Imbalance Cost\n(w/o PIU)\n$/MWh'] = ((gip_net_hourly_income - hourly_zero_imbalance)[plants_under_org].mean()/ total_prod).round(2)
            df.loc[org, 'KGUP Cost\n(w/o PIU)\nTL/MWh'] = ((plant_wise_data['KGUP Cost\n(w/o PIU)\nTL/MWh']*production.sum()).sum()/total_prod).round(2)
            df.loc[org, 'Zero Imbalance\nUnit Price\n(with YEKBED)\n$/MWh'] = ((plant_wise_data['Zero Imbalance\nUnit Price\n(with YEKBED)\n$/MWh']*production.sum()).sum()/total_prod).round(2)
            df.loc[org, 'Organization\nUnit Price\n(w/o GIP)\n$/MWh'] = ((yekbed + dam_net_hourly_income[plants_under_org].mean())/total_prod).round(2)
            df.loc[org, 'Organization\nUnit Price\nAfter GIP\n$/MWh'] = ((yekbed + gip_net_hourly_income[plants_under_org].mean())/total_prod).round(2)
            df.loc[org, 'Organization\nUnit Price\nAfter Imb Sharing\n$/MWh'] = ((yekbed + gip_net_hourly_income_edt_shared[plants_under_org].mean())/total_prod).round(2)

        df['Date'] = self.month
        df.index.name = 'Organizations'
        df.to_excel(paths.reports_data_path + self.month_for_path + f'/output-org-{self.month}.xlsx')
        return df

    def run_type_wise(self, data, df_plant_wise):
        types = self.config['type'].unique()
        df = pd.DataFrame()
        for t in types:
            plants_under_org = self.config[self.config['type'] == t].index
            plant_wise_data = df_plant_wise.loc[plants_under_org, :]
            production = data.production[plants_under_org]
            total_prod = production.sum(axis=1).sum()
            for c in df_plant_wise.columns:
                if c != 'Date' and c != 'org':
                    df.loc[t, c] = ((plant_wise_data[c] * production.sum()).sum() / total_prod).round(4)
            for c in df_plant_wise.columns[0:5]:
                df.loc[t, c] = round((plant_wise_data[c]).sum(), 0)
        df['Date'] = self.month
        df.index.name = 'Power Plants'
        df['org'] = constants.org_names
        df = df.append(df_plant_wise)
        df = df[constants.report_cols]
        df.to_excel(paths.reports_data_path + self.month_for_path + f'/output-{self.month}.xlsx')
        return df


    @staticmethod
    def calculate_hourly_imbalance_cost(imbalance, ptf_smf):
        """
        :param imbalance:
        :param ptf_smf:
        :return:
        """
        negative_imbalance_price = ptf_smf.max(axis=1) * 1.03
        positive_imbalance_price = ptf_smf.min(axis=1) * 0.97
        negative_imbalance_cost = imbalance[imbalance < 0].mul(negative_imbalance_price, axis=0).fillna(0)
        positive_imbalance_cost = imbalance[imbalance > 0].mul(positive_imbalance_price, axis=0).fillna(0)
        imbalance_cost = negative_imbalance_cost + positive_imbalance_cost

        return imbalance_cost

    @staticmethod
    def calculate_hourly_kupst(ref, data):
        deviation = abs(ref - data.production)

        kupsm_condition = (deviation > ref * 0.1)
        kupsm = (deviation - ref * 0.1)[kupsm_condition]
        kupsm = kupsm.reindex(ref.index).fillna(0)

        return kupsm.mul(data.ptf_smf[['mcp', 'smp']].max(axis=1) * 0.03, axis=0)
