"""
Файл с парсингом данных с Binance
"""
from pasrsers.api_keys import BINANCE_SECRET, BINANCE_PUBLIC
from pprint import pprint

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


def parse_binance_p2p(action, asset, bank):
    fiat = 'RUB'
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


def pasrse_all_p2p():
    acns = ['BUY', 'SELL']
    assets = ['USDT', 'BTC', 'ETH']
    banks = ['TinkoffNew', 'RaiffeisenBank']
    p2p_prices = []
    for b in banks:
        for ass in assets:
            rb = parse_binance_p2p('BUY', ass, b)
            rs = parse_binance_p2p('SELL', ass, b)
            p2p_prices.append({'price': rb[0]['price'], 'asset': ass, 'bank': b, 'action': 'BUY'})
            p2p_prices.append({'price': rs[0]['price'], 'asset': ass, 'bank': b, 'action': 'SELL'})
    return p2p_prices


def get_spot_data():
    def split_symbol(symbol):
        for i in range(len(symbol)):
            s1 = symbol[0:2 + i]
            s2 = symbol[2 + i::]
            if s1 in all_coins_names_set and s2 in all_coins_names_set:
                return s1, s2
        return None, None

    spot_data = {}
    all_coins_names_set = set(map(lambda x: x['coin'], client.get_all_coins_info()))  # вынести в инициализацию
    symbols = list(map(lambda x: x['symbol'], client.get_all_tickers()))
    orderbooks = client.get_orderbook_tickers()
    for ob in orderbooks:
        symbol = ob['symbol']
        if float(ob['bidQty']) > 0 and float(ob['askQty']) > 0:
            token_a, token_b = split_symbol(symbol)
            spot_data[(token_a, token_b)] = {"from_token": token_a,
                                             "to_token": token_b,
                                             "price": float(ob['bidPrice'])}
            spot_data[(token_b, token_a)] = {"from_token": token_a,
                                             "to_token": token_b,
                                             "price": 1 / float(ob['askPrice'])}
    return spot_data


def get_binance_data():
    """
    Возвращает данные о Бинансе(spot и p2p)
    :return:
    """

    return get_spot_data(), pasrse_all_p2p()


if __name__ == '__main__':
    from binance.client import Client

    client = Client(BINANCE_PUBLIC, BINANCE_SECRET)
    sd = get_binance_data()
    pprint(sd)
