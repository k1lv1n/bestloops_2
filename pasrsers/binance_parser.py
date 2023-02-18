"""
Файл с парсингом данных с Binance
"""
import fake_useragent
import requests


def get_data_for_request_binance_p2p(action, fiat, asset, bank):
    cookies = {
        'common_fiat': fiat,
    }

    headers = {
        'referer': 'https://p2p.binance.com/trade/' + bank + '/' + asset + '?fiat=' + fiat,
        'user-agent': fake_useragent.UserAgent().random,
    }

    json_data = {
        'proMerchantAds': False,
        'page': 1,
        'rows': 10,
        'payTypes': [bank, ],
        'countries': [],
        'publisherType': None,
        'asset': asset,
        'fiat': fiat,
        'tradeType': action,
    }

    return cookies, headers, json_data


def parse_binance_p2p(action, fiat, asset, bank):
    data_for_request = get_data_for_request_binance_p2p(action, fiat, asset, bank)
    cookies = data_for_request[0]
    headers = data_for_request[1]
    json_data = data_for_request[2]

    response = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
                             cookies=cookies, headers=headers, json=json_data)

    response_json = response.json()["data"]  # Тут очень много данных, возвращаем лишь малую часть

    parsed_data = []

    # TODO проитерироваться по всем fiat тикерам, Tinkof теперь TinkofNew вроде

    for data in response_json:
        parsed_data.append(
            {
                'price': data['adv']['price'],
                'volume': data['adv']['surplusAmount'],
                'min_limit': data['adv']['minSingleTransAmount'],
                'max_limit': data['adv']['maxSingleTransAmount'],
            }
        )

    return parsed_data


def get_binance_data():
    """
    Возвращает данные о Бинансе(spot и p2p)
    :return:
    """

    return None, None
