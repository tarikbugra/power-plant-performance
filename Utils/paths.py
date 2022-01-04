import os

pdf_font = os.path.join(supplementaries_path, 'Font/DejaVuSans.ttf')
pdf_font_Bold = os.path.join(supplementaries_path, 'Font/DejaVuSans-Bold.ttf')


db_path = root_path + '/Desktop/uzl'


def prepare_paths(date):
    global kudup_path, eak_path, currency_path, mcp_smp_path, gop_org_total, prod_org_total, gip_org_total, config
    global pp_basis_path, multiple_dam_path
    create_directories(date)
    kudup_path = os.path.join(one_drive_path, 'company/KGUP/' + date.month + '-KUDUP.xls')
    eak_path = os.path.join(one_drive_path, 'company/KGUP/' + date.month + '-EAK.xls')
    currency_path = os.path.join(one_drive_path, 'company/KUR/' + date.month + '-kur.xlsx')
    mcp_smp_path = os.path.join(one_drive_path, 'company/PTF-SMF/' + date.month + '-ptf_smf.xlsx')
    gop_org_total = os.path.join(one_drive_path, 'company/GOP/' + date.month + '-GOP.xls')
    prod_org_total = os.path.join(one_drive_path, 'company/Real_production/' + date.month + '.xls')
    gip_org_total = os.path.join(one_drive_path, 'company/Results/' + date.month + '-im-net-positions.xlsx')
    config = os.path.join(supplementaries_path + '/Config/' + date.year + '/config_file-' + date.month + '.xlsx')
    pp_basis_path = os.path.join(database_path, 'Data/' + date.month_for_path + '/' + date.month + '-pp_basis_dam.xlsx')
    multiple_dam_path = os.path.join(dropbox_path, date.month.replace('-', '.') + '.xlsm')


def create_directories(date):
    if not os.path.exists(database_path + 'Data/' + date.year):
        os.makedirs(database_path + 'Data/' + date.year)
    if not os.path.exists(database_path + 'Reports/' + date.month_for_path):
        os.makedirs(database_path + 'Reports/' + date.month_for_path)
    if not os.path.exists(database_path + 'Reports_Data/' + date.month_for_path):
        os.makedirs(database_path + 'Reports_Data/' + date.month_for_path)
