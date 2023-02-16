"""
Файл с парсингом данных с Binance
"""
from pasrsers.api_keys import BINANCE_SECRET, BINANCE_PUBLIC
from pprint import pprint


def split_symbol(symbol):
    for i in range(len(symbol)):
        s1 = symbol[0:2 + i]
        s2 = symbol[2 + i::]
        if s1 in all_coins_names_set and s2 in all_coins_names_set:
            return s1, s2
    return None, None


def get_spot_data():
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

    return None, None


if __name__ == '__main__':
    from binance.client import Client

    client = Client(BINANCE_PUBLIC, BINANCE_SECRET)
    all_coins_names_set = set(map(lambda x: x['coin'], client.get_all_coins_info()))
    sd = get_spot_data()
    pprint(sd)
