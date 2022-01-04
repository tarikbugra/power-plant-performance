import pandas as pd
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from Utils import paths, constants


def app(date, config, report_header='Power Plants', report_tail=''):
    pdfmetrics.registerFont(TTFont('DejaVuSans', paths.pdf_font))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', paths.pdf_font_Bold))

    data_pps = append_last_13_months(date.next_month, date.month_for_path, report_header, report_tail)

    elements = []
    report_name = date.month_for_path + f'/{date.day_str}-Kupst_{report_tail}Report' + '.pdf'
    doc = SimpleDocTemplate(
        filename=paths.reports_path + report_name,
        pagesize=(20 * inch, 9.4 * inch),  # 20/12.4   -   20/9.4
        showBoundary=0,
        leftMargin=inch * 0.5,
        rightMargin=inch * 0.5,
        topMargin=inch * 0.9, #1.3
        bottomMargin=inch * 0.9, #1
        allowSplitting=1,
        title=None,
        author=None,
        _pageBreakQuick=1,
        encrypt=None)

    lista_pps = [data_pps.columns[:, ].values.astype(str).tolist()] + data_pps.values.tolist()
    c_size = len(data_pps.columns)-1
    ts_pps = [('ALIGN', (0, 0), (1, -1), 'LEFT'),
              ('ALIGN', (2, 0), (c_size, -1), 'CENTER'),
              ('FONT', (0, 0), (-1, -1), 'DejaVuSans'),
              ('FONT', (0, 0), (1, -1), 'DejaVuSans-Bold'),
              ('BACKGROUND', (0, 0), (c_size, 0), colors.orange),
              ('FONT', (0, 0), (c_size, 0), 'DejaVuSans-Bold'),
              ('TEXTCOLOR', (0, 0), (1, -1), colors.black),
              ('TEXTCOLOR', (11, 1), (12, -1), colors.red),
              ('FONT', (11, 1), (12, -1), 'DejaVuSans-Bold')]
    #('TEXTCOLOR', (0, 901), (18, -1), colors.purple)

    table_pps = Table(lista_pps, style=ts_pps, repeatRows=1)

    rowNumb_pps = len(lista_pps)

    for i in range(1, rowNumb_pps):
        if i % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige

        ts_background = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)])
        table_pps.setStyle(ts_background)

    for k in range(0, rowNumb_pps):
        if k % 13 == 1 & 2 & 3:
            ts_linebelow = TableStyle(
                [('LINEBELOW', (0, k), (-1, k), 2, colors.black)])
            table_pps.setStyle(ts_linebelow)

    elements.append(table_pps)
    doc.build(elements)


def append_last_13_months(last_month, month_for_path, config, name='Power Plants',  pdf_type=''):
    #get previous data
    r = pd.date_range(end=last_month, periods=13, freq='M', closed='right')
    r_list = [month.strftime('%Y-%m') for month in r]
    list_of_data = [pd.read_excel(paths.reports_data_path + month_for_path + f'/output-{pdf_type}{month}.xlsx') for month in r_list]
    all_data = pd.concat(list_of_data)
    #format data
    if name == 'Power Plants':
        plants = list(constants.org_names.index) + list(config.report_name.values)
        all_data = format_data(all_data)
    else:
        plants = config.org_name.unique()
    all_data = all_data.set_index(name).loc[plants, :].reset_index()
    all_data.sort_values([name, 'Date'], inplace=True)
    data = pd.DataFrame()
    for p in plants:
        plant_data = all_data[all_data[name] == p]
        plant_data = plant_data.set_index('Date').reindex(r_list).reset_index()
        plant_data[name] = p
        data = data.append(plant_data, ignore_index=True)
    data.fillna('-', inplace=True)
    data.loc[data[name].duplicated(), name] = None
    return data


def format_data(all_data):
    all_data.drop('org', axis=1, inplace=True)
    all_data[['Intraday\nMape', 'Day-Ahead\nMape']] = all_data[['Intraday\nMape', 'Day-Ahead\nMape']].applymap('{:.2%}'.format)
    for c in all_data.columns[2:11]:
        all_data[c] = all_data[c].apply(lambda x: format(int(x), ' ,d'))
    for c in all_data.columns[11:17]:
        all_data[c] = all_data[c].apply(lambda x: round(x, 2) if not isinstance(x, str) else x)
    return all_data
