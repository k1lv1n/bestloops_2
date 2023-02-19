"""
Файл с обработкой входящей информации от парсеров. Возможно, если в итоге run.py будет работать слишком долго, то
архитектуру будем бить на недо-сервисы.
"""

from pasrsers.bestchange_parser import *
from pasrsers.binance_parser import *
from pasrsers.garantex_parser import *


def find_paths(bestchange_data_banks,
               bestchange_data_usdt,
               binance_spot_data,
               binance_p2p_data, binance_coins, garantex_data):
    """
    Функция вычисления арбитражных возможностей
    :param bestchange_data_usdt:
    :param bestchange_data_banks:
    :param binance_coins:
    :param binance_spot_data: данные о споте бинанса
    :param binance_p2p_data: данные о п2п бинанса
    :param garantex_data: данные о гарантексе
    :return:
    """
    coins_to_p2p = ['BTC', 'USDT', 'ETH', 'RUB']
    routes_banks = []
    for bch_pair in bestchange_data_banks:
        coin = bch_pair['coin']
        amount_0 = 1_000_000 / bch_pair['rate']
        for bcoin in binance_coins:
            if bcoin not in ['NGN']:
                try:
                    amount_1 = amount_0 * binance_spot_data[(coin, bcoin)]['price']
                except KeyError:
                    continue
                for ccoin in coins_to_p2p:
                    try:
                        amount_2 = amount_1 * binance_spot_data[(bcoin, ccoin)]['price']
                    except KeyError:
                        continue
                    for bank in ['TinkoffNew', 'RaiffeisenBank', 'RosBankNew']:
                        amount_3 = amount_2 * float(binance_p2p_data[(bank, ccoin, 'BUY')]['price'])
                        if amount_3 > 1_000_000 * (1 + 0.1 / 100):
                            routes_banks.append((bch_pair['bank'], coin, bcoin, ccoin, bank, amount_3,
                                                 bch_pair['rate'],
                                                 binance_spot_data[(coin, bcoin)]['price'],
                                                 binance_spot_data[(bcoin, ccoin)]['price'],
                                                 float(binance_p2p_data[(bank, ccoin, 'BUY')]['price'])))
    routes_usdt = []
    for bch_pair in bestchange_data_usdt:
        coin = bch_pair['coin']
        amount_0 = 1_000_000 / bch_pair['rate']
        for bcoin in binance_coins:
            if bcoin not in ['NGN']:
                try:
                    amount_1 = amount_0 * binance_spot_data[(coin, bcoin)]['price']
                    amount_2 = amount_1 * binance_spot_data[(bcoin, 'USDT')]['price']
                    if amount_2 > 1_000_000:
                        routes_usdt.append(('usdt', coin, bcoin, 'usdt', amount_2))
                except KeyError:
                    continue

    routes_bingar = []
    coins_bingar = ['BTC', 'USDT', 'ETH']
    banks = ['TinkoffNew', 'RaiffeisenBank', 'RosBankNew']
    for coin in coins_bingar:
        for b in banks:
            bin_price_sell = binance_p2p_data[(b, coin, 'SELL')]['price']
            bin_price_buy = binance_p2p_data[(b, coin, 'BUY')]['price']
            gar_price = garantex_data[coin.lower() + 'rub']
            if gar_price['bids_price'] > bin_price_sell:
                routes_bingar.append((b, bin_price_sell, gar_price['bids_price'], coin, 'some profit'))
            if gar_price['asks_price'] < bin_price_buy:
                routes_bingar.append((gar_price['asks_price'], b, bin_price_buy, coin, 'some_profit'))
    return routes_banks, routes_usdt, routes_bingar


if __name__ == '__main__':
    bestchange_data_banks, bestchange_data_usdt = get_bestchange_data()
    (binance_spot_data, binance_coins), binance_p2p_data = get_binance_data()
    garantex_data = get_garantex_data()
    pprint(find_paths(bestchange_data_banks, bestchange_data_usdt, binance_spot_data,
                      binance_p2p_data, binance_coins, garantex_data))
