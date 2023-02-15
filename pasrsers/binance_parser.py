"""
Файл с парсингом данных с Binance
"""
from pasrsers.api_keys import BINANCE_SECRET, BINANCE_PUBLIC


def get_binance_data():
    """
    Возвращает данные о Бинансе(spot и p2p)
    :return:
    """

    return None, None


if __name__ == '__main__':
    from binance.client import Client

    client = Client(BINANCE_PUBLIC, BINANCE_SECRET)
    ALL_COIN_NAMES = [cur['coin'] for cur in client.get_all_coins_info()] + ["RUB"]
    ALL_COIN_NAMES_D = {cur['coin']: 0 for cur in client.get_all_coins_info()}
    res = client.get_all_coins_info()
    print(res)
