"""
Файл с обработкой входящей информации от парсеров. Возможно, если в итоге run.py будет работать слишком долго, то
архитектуру будем бить на недо-сервисы.
"""


def find_paths(bestchange_data,
               binance_spot_data,
               binance_p2p_data, garantex_data):
    """
    Функция вычисления арбитражных возможностей
    :param bestchange_data: данные об обменниках
    :param binance_spot_data: данные о споте бинанса
    :param binance_p2p_data: данные о п2п бинанса
    :param garantex_data: данные о гарантексе
    :return:
    """
