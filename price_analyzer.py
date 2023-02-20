"""
Файл с обработкой входящей информации от парсеров. Возможно, если в итоге run.py будет работать слишком долго, то
архитектуру будем бить на недо-сервисы.
"""

from bestloops_2.pasrsers.bestchange_parser import *
from bestloops_2.pasrsers.binance_parser import *
from bestloops_2.pasrsers.garantex_parser import *


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
        amount_0 = 100_000 / bch_pair['rate']
        for bcoin in coins_to_p2p:
            try:
                amount_1 = amount_0 * binance_spot_data[(coin, bcoin)]['price']
            except KeyError:
                continue
            for bank in ['TinkoffNew', 'RaiffeisenBank', 'RosBankNew']:
                amount_2 = amount_1 * float(binance_p2p_data[(bank, bcoin, 'BUY')]['price'])
                if amount_2 < 100_000:  # TODO поменять на >
                    routes_banks.append({
                        'exch_name': bch_pair['exchangers'],
                        'bank_init': bch_pair['bank'],
                        'bch_coin': coin,
                        'binance_coin': bcoin,
                        'end_bank': bank,
                        'middle_amount': amount_1,
                        'final_amount': amount_2,
                        'init_amount': amount_0,
                        'bch_rate': bch_pair['rate'],
                        'binance_rate_spot': binance_spot_data[(coin, bcoin)]['price'],
                        'binance_rate_p2p': float(binance_p2p_data[(bank, bcoin, 'BUY')]['price']),
                        'href': bch_pair['href'],
                        'binance_href': binance_spot_data[(coin, bcoin)]['href']
                    })

    routes_usdt = []
    for bch_pair in bestchange_data_usdt:
        coin = bch_pair['coin']
        amount_0 = 1_000 / bch_pair['rate']
        for bcoin in binance_coins:
            if bcoin not in ['NGN']:
                try:
                    # TODO А что если выгоднее USDT -> COIN_A -> USDT ?
                    amount_1 = amount_0 * binance_spot_data[(coin, bcoin)]['price']
                    amount_2 = amount_1 * binance_spot_data[(bcoin, 'USDT')]['price']
                    if amount_2 > 1_000:
                        routes_usdt.append({
                            'exch_name': bch_pair['exchangers'],
                            'init_coin': 'usdt',
                            'bch_coin': coin,
                            'binance_coin': bcoin,
                            'bch_rate': bch_pair['rate'],
                            'binance_coin_bcoin_rate': binance_spot_data[(coin, bcoin)]['price'],
                            'binance_bcoin_usdt_rate': binance_spot_data[(bcoin, 'USDT')]['price'],
                            'amount_0': amount_0,
                            'middle_amount': amount_1,
                            'final_amount': amount_2,
                            'href': bch_pair['href'],
                            'binance_href_coin_to_b': binance_spot_data[(coin, bcoin)]['href'],
                            'binance_href_b_to_usdt': binance_spot_data[(bcoin, 'USDT')]['href']
                        })
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
                routes_bingar.append({
                    'path': 0,  # Binance -> Garantex
                    'bank': b,
                    'binance_p2p_price': float(bin_price_sell),
                    'garantex_price': float(gar_price['bids_price']),
                    'coin': coin
                })
            if gar_price['asks_price'] < bin_price_buy:
                routes_bingar.append({
                    'path': 1,  # Garantex -> Binance
                    'bank': b,
                    'binance_p2p_price': float(bin_price_buy),
                    'garantex_price': float(gar_price['asks_price']),
                    'coin': coin
                })
    return routes_banks, routes_usdt, routes_bingar


if __name__ == '__main__':
    bestchange_data_banks, bestchange_data_usdt = get_bestchange_data()
    (binance_spot_data, binance_coins), binance_p2p_data = get_binance_data()
    garantex_data = get_garantex_data()
    pprint(find_paths(bestchange_data_banks, bestchange_data_usdt, binance_spot_data,
                      binance_p2p_data, binance_coins, garantex_data))
