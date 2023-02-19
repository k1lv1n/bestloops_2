"""
Файл с функциями отправки сообщений по каналам. Скорее всего в итоге он будет иметь другой вид.
"""
import aiogram
from aiogram import Bot, types, Dispatcher, executor

from bestloops_2.pasrsers.bestchange_parser import get_bestchange_data
from bestloops_2.pasrsers.binance_parser import get_binance_data
from bestloops_2.pasrsers.garantex_parser import get_garantex_data
from configs import BOT_TOKEN, TEST_CHANNEL_ID, SBER_LESS_THAN_ONE_CHANNEL_ID, TINK_LESS_THAN_ONE_CHANNEL_ID, \
    VIP_CHANNEL_ID, NO_BANK_CHANNEL_ID, BINANCE_GARANTEX_CHANNEL_ID
import asyncio
from bestloops_2.price_analyzer import find_paths
import datetime

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def send_to_sber_less_then_one(data_to_be_sent):
    for message in data_to_be_sent:
        try:
            await bot.send_message(chat_id=SBER_LESS_THAN_ONE_CHANNEL_ID, text=message, parse_mode='Markdown')
        except aiogram.exceptions.RetryAfter:
            continue


async def send_to_tink_less_then_one(data_to_be_sent):
    for message in data_to_be_sent:
        try:
            await bot.send_message(chat_id=TINK_LESS_THAN_ONE_CHANNEL_ID, text=message, parse_mode='Markdown')
        except aiogram.exceptions.RetryAfter:
            continue


async def send_to_vip(data_to_be_sent):
    for message in data_to_be_sent:
        try:
            await bot.send_message(chat_id=VIP_CHANNEL_ID, text=message, parse_mode='Markdown')
        except aiogram.exceptions.RetryAfter:
            continue


async def send_to_binance_garantex(data_to_be_sent):
    for message in data_to_be_sent:
        try:
            await bot.send_message(chat_id=BINANCE_GARANTEX_CHANNEL_ID, text=message, parse_mode='Markdown')
        except aiogram.exceptions.RetryAfter:
            continue


async def send_to_no_bank(data_to_be_sent):
    for message in data_to_be_sent:
        try:
            await bot.send_message(chat_id=NO_BANK_CHANNEL_ID, text=message, parse_mode='Markdown')
        except aiogram.exceptions.RetryAfter:
            continue


async def send_to_test(data_to_be_sent):
    for message in data_to_be_sent[0:10]:
        try:
            await bot.send_message(chat_id=TEST_CHANNEL_ID, text=message, parse_mode='Markdown')
        except aiogram.exceptions.RetryAfter:
            continue


def from_text_tink_less_then_one(routes):
    max_messages = 5
    messages = []
    sorted_routs = sorted(routes, key=lambda x: x['final_amount'] / 100_000, reverse=True)
    for r in sorted_routs:
        profit = round(100 * (r["final_amount"] / 100_000 - 1), 2)
        if profit >= 1 and r["bank_init"] != 'tinkoff':
            continue
        else:
            text = r["bank_init"] + ' -> ' + r['bch_coin'] + ' -> ' + r['binance_coin'] + ' -> ' + r['end_bank'] \
                   + '\n' + f'profit: *{profit} %*' + '\n\n' + f'Обменник: {r["exch_name"]}' + '\n' \
                   + 'Обмениваем на bestchange: ' + '100 000 рублей ' + r[
                       'bank_init'] + '\n' + 'Получаем на binance: ' + f'{round(100_000 / r["bch_rate"], 2)}' + f' {r["bch_coin"]}' + '\n' \
                   + 'Продаем на binance spot ' + f'{r["bch_coin"]}' + ' по курсу' + f' {round(r["binance_rate_spot"], 5)}' + f'\nПолучаем {round(r["middle_amount"], 2)} {r["binance_coin"]}' \
                   + f'\nПродаем {r["binance_coin"]}' + f' на binance p2p по курсу {r["binance_rate_p2p"]}' \
                   + f'\nПолучаем на {r["end_bank"]} {round(r["final_amount"], 2)}'
            messages.append(text)
            max_messages -= 1
        if max_messages == 0:
            break
    return messages


def form_text_sber_less_then_one(routes):
    max_messages = 5
    messages = []
    sorted_routs = sorted(routes, key=lambda x: x['final_amount'] / 100_000, reverse=True)
    for r in sorted_routs:
        profit = round(100 * (r["final_amount"] / 100_000 - 1), 2)
        if profit >= 1 and r["bank_init"] != 'sber':
            continue
        else:
            text = r["bank_init"] + ' -> ' + r['bch_coin'] + ' -> ' + r['binance_coin'] + ' -> ' + r['end_bank'] \
                   + '\n' + f'profit: *{profit} %*' + '\n\n' + f'Обменник: {r["exch_name"]}' + '\n' \
                   + 'Обмениваем на bestchange: ' + '100 000 рублей ' + r[
                       'bank_init'] + '\n' + 'Получаем на binance: ' + f'{round(100_000 / r["bch_rate"], 2)}' + f' {r["bch_coin"]}' + '\n' \
                   + 'Продаем на binance spot ' + f'{r["bch_coin"]}' + ' по курсу' + f' {round(r["binance_rate_spot"], 5)}' + f'\nПолучаем {round(r["middle_amount"], 2)} {r["binance_coin"]}' \
                   + f'\nПродаем {r["binance_coin"]}' + f' на binance p2p по курсу {r["binance_rate_p2p"]}' \
                   + f'\nПолучаем на {r["end_bank"]} {round(r["final_amount"], 2)}'
            messages.append(text)
            max_messages -= 1
        if max_messages == 0:
            break
    return messages


def form_text_vip(routes):
    max_messages = 5
    messages = []
    sorted_routs = sorted(routes, key=lambda x: x['final_amount'] / 100_000, reverse=True)
    for r in sorted_routs:
        profit = round(100 * (r["final_amount"] / 100_000 - 1), 2)
        if profit < 1:
            continue
        else:
            text = r["bank_init"] + ' -> ' + r['bch_coin'] + ' -> ' + r['binance_coin'] + ' -> ' + r['end_bank'] \
                   + '\n' + f'profit: *{profit} %*' + '\n\n' + f'Обменник: {r["exch_name"]}' + '\n' \
                   + 'Обмениваем на bestchange: ' + '100 000 рублей ' + r[
                       'bank_init'] + '\n' + 'Получаем на binance: ' + f'{round(100_000 / r["bch_rate"], 2)}' + f' {r["bch_coin"]}' + '\n' \
                   + 'Продаем на binance spot ' + f'{r["bch_coin"]}' + ' по курсу' + f' {round(r["binance_rate_spot"], 5)}' + f'\nПолучаем {round(r["middle_amount"], 2)} {r["binance_coin"]}' \
                   + f'\nПродаем {r["binance_coin"]}' + f' на binance p2p по курсу {r["binance_rate_p2p"]}' \
                   + f'\nПолучаем на {r["end_bank"]} {round(r["final_amount"], 2)}'
            messages.append(text)
            max_messages -= 1
        if max_messages == 0:
            break
    return messages


async def start_sending():
    while True:
        bestchange_data_banks, bestchange_data_usdt = get_bestchange_data()
        (binance_spot_data, binance_coins), binance_p2p_data = get_binance_data()
        garantex_data = get_garantex_data()
        routes_banks, routes_usdt, routes_bingar = find_paths(bestchange_data_banks, bestchange_data_usdt,
                                                              binance_spot_data,
                                                              binance_p2p_data, binance_coins, garantex_data)
        print(datetime.datetime.now())
        print('BANKS  ', routes_banks)
        print('USDT  ', routes_usdt)  # ('usdt', 'LTC', 'BUSD', 'usdt', 1000095.4305271294)
        print('BINGAR  ', routes_bingar)  # [('1894700.0', 'TinkoffNew', '1902490.99', 'BTC', 'some_profit') GAR -> BIN
        # ('RaiffeisenBank', '1889202.72', '1894454.41', 'BTC', 'some profit') BIN -> GAR
        coros = [send_to_vip(form_text_vip(routes_banks)),
                 send_to_sber_less_then_one(form_text_sber_less_then_one(routes_banks)),
                 send_to_tink_less_then_one(from_text_tink_less_then_one(routes_banks))]
        await asyncio.gather(*coros)
        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(start_sending())
