"""
Created on Thu Jul 18 14:58:34 2019

@author: Bugra
"""

from DataFetcher import utilsx


def get_dam_matching_result(startDate, endDate, eic):
    """
    Returns DAM matching results between startDate and endDate for organization with ETSO=eic
    :param startDate: String
    :param endDate: String
    :param eic: String
    """
    url_tail = 'market/day-ahead-market-volume?startDate=' + startDate + '&endDate=' + endDate + '&eic=' + eic
    url_header = 'dayAheadMarketVolumeList'
    data = utilsx.get_data_from_rest_service(url_tail, url_header)
    return data


def get_bilateral_sell_result(startDate, endDate, eic):
    """
    Returns bilateral sell results between startDate and endDate for organization with ETSO=eic
    :param startDate: String
    :param endDate: String
    :param eic: String
    """
    url_tail = 'market/bilateral-contract-sell?startDate=' + startDate + '&endDate=' + endDate + '&eic=' + eic
    url_header = 'bilateralContractSellList'
    data = utilsx.get_data_from_rest_service(url_tail, url_header)
    return data


def get_bilateral_buy_result(startDate, endDate, eic):
    """
    Returns bilateral sell results between startDate and endDate for organization with ETSO=eic
    :param startDate: String
    :param endDate: String
    :param eic: String
    """
    url_tail = 'market/bilateral-contract-buy?startDate=' + startDate + '&endDate=' + endDate + '&eic=' + eic
    url_header = 'bilateralContractBuyList'
    data = utilsx.get_data_from_rest_service(url_tail, url_header)
    return data


def get_real_time_production(startDate, endDate, powerPlantId):
    """
    Returns real time production etween startDate and endDate for plant id with santralId
    :param startDate: String
    :param endDate: String
    :santradId: String
    """
    url_tail = 'production/real-time-generation_with_powerplant?startDate=' + startDate + '&endDate=' + endDate + '&powerPlantId=' + powerPlantId
    url_header = 'hourlyGenerations'
    data = utilsx.get_data_from_rest_service(url_tail, url_header)
    return data


def get_mcp_smp(startDate, endDate):
    """
    Returns real time production etween startDate and endDate for plant id with santralId
    :param startDate: String
    :param endDate: String
    :santradId: String
    """
    url_tail = 'market/mcp-smp?startDate=' + startDate + '&endDate=' + endDate
    url_header = 'mcpSmps'
    data = utilsx.get_data_from_rest_service(url_tail, url_header)
    return data


def get_intraday_summary_hourly(startDate, endDate, offerType):
    """
    Returns real time production etween startDate and endDate for plant id with santralId
    :param startDate: String
    :param endDate: String
    :santradId: String
    """
    url_tail = 'market/intra-day-summary?startDate=' + startDate + '&endDate=' + endDate + '&offerType=' + offerType
    url_header = 'intraDaySummaryList'
    data = utilsx.get_data_from_rest_service(url_tail, url_header)
    return data


def get_intraday_summary_block(startDate, endDate, offerType):
    """
    Returns real time production etween startDate and endDate for plant id with santralId
    :param startDate: String
    :param endDate: String
    :santradId: String
    """
    url_tail = 'market/intra-day-summary?startDate=' + startDate + '&endDate=' + endDate + '&offerType=' + offerType
    url_header = 'intraDaySummaryList'
    data = utilsx.get_data_from_rest_service(url_tail, url_header)
    return data


def get_kudup(startDate, endDate, organizationId, uevcbId):
    """
    Returns real time production etween startDate and endDate for plant id with santralId
    :param startDate: String
    :param endDate: String
    :santradId: String
    """
    url_tail = 'production/sbfgp?startDate=' + startDate + '&organizationId=' + organizationId + '&endDate=' + endDate + '&uevcbId=' + uevcbId
    url_header = 'dppList'
    data = utilsx.get_data_from_rest_service(url_tail, url_header)
    return data


def get_4pm_kgup(startDate, endDate, organizationEIC, uevcbEIC):
    """
    Returns real time production etween startDate and endDate for plant id with santralId
    :param startDate: String
    :param endDate: String
    :santradId: String
    """
    url_tail = 'production/dpp?startDate=' + startDate + '&organizationEIC=' + organizationEIC + '&uevcbEIC=' + uevcbEIC + '&endDate=' + endDate
    url_header = 'dppList'
    data = utilsx.get_data_from_rest_service(url_tail, url_header)
    return data


def get_eak(startDate, endDate, organizationEIC, uevcbEIC):
    """
    Returns real time production etween startDate and endDate for plant id with santralId
    :param startDate: String
    :param endDate: String
    :santradId: String
    """
    url_tail = 'production/aic?startDate=' + startDate + '&organizationEIC=' + organizationEIC + '&uevcbEIC=' + uevcbEIC + '&endDate=' + endDate
    url_header = 'aicList'
    data = utilsx.get_data_from_rest_service(url_tail, url_header)
    return data


def get_renewable_Unlicenced_Generation(startDate, endDate):
    """
    Returns real time production etween startDate and endDate for plant id with santralId
    :param startDate: String
    :param endDate: String
    :santradId: String
    """
    url_tail = 'production/renewable-unlicenced-generation-amount?startDate=' + startDate + '&endDate=' + endDate
    url_header = 'renewableUnlicencedGenerationAmountList'
    data = utilsx.get_data_from_rest_service(url_tail, url_header)
    return data
