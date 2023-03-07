"""
Файл с функциями отправки сообщений по каналам. Скорее всего в итоге он будет иметь другой вид.
"""
import aiogram
from aiogram import Bot, Dispatcher
import os
import sys
#sys.path.append("..")
sys.path.append("/root/bestloops_2/")
from pasrsers.bestchange_parser import get_bestchange_data
from pasrsers.binance_parser import get_binance_data
from pasrsers.garantex_parser import get_garantex_data
from configs import BOT_TOKEN, TEST_CHANNEL_ID, SBER_LESS_THAN_ONE_CHANNEL_ID, TINK_LESS_THAN_ONE_CHANNEL_ID, \
    VIP_CHANNEL_ID, NO_BANK_CHANNEL_ID, BINANCE_GARANTEX_CHANNEL_ID
import asyncio
from price_analyzer import find_paths
import time

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def send_to_sber_less_then_one(data_to_be_sent):
    if len(data_to_be_sent) == 0:
        return None
    try:
        await bot.send_message(chat_id=SBER_LESS_THAN_ONE_CHANNEL_ID,
                               text='________________________________________')
    except aiogram.exceptions.RetryAfter:
        pass
    for message in data_to_be_sent:
        try:
            await bot.send_message(chat_id=SBER_LESS_THAN_ONE_CHANNEL_ID, text=message, parse_mode='Markdown')
        except aiogram.exceptions.RetryAfter:
            continue


async def send_to_tink_less_then_one(data_to_be_sent):
    if len(data_to_be_sent) == 0:
        return None
    try:
        await bot.send_message(chat_id=TINK_LESS_THAN_ONE_CHANNEL_ID,
                               text='________________________________________')
    except aiogram.exceptions.RetryAfter:
        pass
    for message in data_to_be_sent:
        try:
            await bot.send_message(chat_id=TINK_LESS_THAN_ONE_CHANNEL_ID, text=message, parse_mode='Markdown')
        except aiogram.exceptions.RetryAfter:
            continue


async def send_to_vip(data_to_be_sent):
    if len(data_to_be_sent) == 0:
        return None
    try:
        await bot.send_message(chat_id=VIP_CHANNEL_ID, text='________________________________________')
    except aiogram.exceptions.RetryAfter:
        pass
    for message in data_to_be_sent:
        try:
            await bot.send_message(chat_id=VIP_CHANNEL_ID, text=message, parse_mode='Markdown')
        except aiogram.exceptions.RetryAfter:
            continue


async def send_to_binance_garantex(data_to_be_sent):
    if len(data_to_be_sent) == 0:
        return None
    try:
        await bot.send_message(chat_id=BINANCE_GARANTEX_CHANNEL_ID,
                               text='________________________________________')
    except aiogram.exceptions.RetryAfter:
        pass
    for message in data_to_be_sent:
        try:
            await bot.send_message(chat_id=BINANCE_GARANTEX_CHANNEL_ID, text=message, parse_mode='Markdown')
        except aiogram.exceptions.RetryAfter:
            continue


async def send_to_no_bank(data_to_be_sent):
    if len(data_to_be_sent) == 0:
        return None
    try:
        await bot.send_message(chat_id=NO_BANK_CHANNEL_ID,
                               text='________________________________________')
    except aiogram.exceptions.RetryAfter:
        pass
    for message in data_to_be_sent:
        try:
            await bot.send_message(chat_id=NO_BANK_CHANNEL_ID, text=message, parse_mode='Markdown')
        except aiogram.exceptions.RetryAfter:
            continue


async def send_to_test(data_to_be_sent):
    if len(data_to_be_sent) == 0:
        return None
    try:
        await bot.send_message(chat_id=TEST_CHANNEL_ID,
                               text='________________________________________')
    except aiogram.exceptions.RetryAfter:
        pass
    for message in data_to_be_sent:
        try:
            await bot.send_message(chat_id=TEST_CHANNEL_ID, text=message, parse_mode='Markdown')
        except aiogram.exceptions.RetryAfter:
            continue


def form_text_bingar(routes):
    max_messages_bin_gar = 5
    max_messages_gar_bin = 5
    messages = []
    sorted_routs = sorted(routes, key=lambda x: x['garantex_price'] / x['binance_p2p_price'] if x['path'] == 0 else x[
                                                                                                                        'binance_p2p_price'] /
                                                                                                                    x[
                                                                                                                        'garantex_price'],
                          reverse=True)
    for r in sorted_routs:
        if r['path'] == 0 and max_messages_bin_gar != 0:  # Binance -> Grantex
            profit = round(100 * (r["final_amount"] / 100_000 - 1), 2)
            text = r['bank'] + ' -> ' + r['coin'] + ' -> ' + 'Garantex' \
                   + '\n' + f'profit: *{profit} %*' + '\n\n' \
                   + f'‣Покупаем на [binance p2p]({r["binance_p2p_href"]}): ' + f'за 100 000 рублей {r["coin"]}' + '\n' + f'*по курсу {r["binance_p2p_price"]}*\n' \
                   + 'Получаем на binance: ' + f'{round(100_000 * (1 - .25 / 100) / r["binance_p2p_price"], 3)}' + f' {r["coin"]}\n' + '\n' \
                   + f'‣Продаем на [Garantex]({r["garantex_href"]}) ' + f'{r["coin"]}' + ' *по курсу' + f' {round(r["garantex_price"], 6)}*' \
                   + f'\nполучаем {r["final_amount"]} рублей'
            messages.append(text)
            max_messages_bin_gar -= 1

        elif r['path'] == 1 and max_messages_gar_bin != 0:  # Garantex -> Binance
            profit = round(100 * (r["final_amount"] / 100_000 - 1), 2)
            text = 'Garantex RUB' + ' -> ' + r['coin'] + ' -> ' + r['bank'] \
                   + '\n' + f'profit: *{profit} %*' + '\n\n' \
                   + f'‣Покупаем на [garantex spot]({r["garantex_href"]}): ' + f'за 100 000 рублей {r["coin"]}' + '\n' + f'*по курсу {r["garantex_price"]}*\n' \
                   + 'Получаем на Garantex: ' + f'{round(100_000 * (1 - .25 / 100) / r["garantex_price"], 3)}' + f' {r["coin"]}\n' + '\n' \
                   + f'‣Продаем на [binance p2p]({r["binance_p2p_href"]}) ' + f'{r["coin"]}' + ' *по курсу' + f' {round(r["binance_p2p_price"], 6)}*' \
                   + f'\nполучаем {r["final_amount"]} рублей ' + r[
                       'bank']
            messages.append(text)
            max_messages_gar_bin -= 1
    return messages


def form_text_usdt(routes):
    max_messages = 5
    messages = []
    sorted_routs = sorted(routes, key=lambda x: x['final_amount'] / 1_000, reverse=True)
    for r in sorted_routs:
        profit = round(100 * (r["final_amount"] / 1_000 - 1), 2)
        text = 'USDT' + ' -> ' + r['bch_coin'] + ' -> ' + r['binance_coin'] + ' -> ' + 'USDT' \
               + '\n' + f'profit: *{profit} %*' + '\n\n' + f'Обменник: {r["exch_name"]}' + '\n\n' \
               + f'‣Обмениваем на [bestchange]({r["href"]}): 1 000 USDT \n' + f'*по курсу {r["bch_rate"]}*\n' + 'получаем на binance: ' + f'{round(1_000 / r["bch_rate"], 3)}' + f' {r["bch_coin"]}\n' + '\n' \
               + f'‣Продаем {r["bch_coin"]} на [binance spot]({r["binance_href_coin_to_b"]}) \n*по курсу' + f' {round(r["binance_coin_bcoin_rate"], 6)}*' + f'\nполучаем {round(r["middle_amount"], 3)} {r["binance_coin"]}' \
               + f'\n\n‣Продаем {r["binance_coin"]}' + f' на [binance spot]({r["binance_href_b_to_usdt"]}) \n*по курсу {r["binance_bcoin_usdt_rate"]}*' \
               + f'\nполучаем USDT {round(r["final_amount"], 3)}'
        messages.append(text)
        max_messages -= 1
        if max_messages == 0:
            break
    return messages


def from_text_tink_less_then_one(routes):
    max_messages = 5
    messages = []
    sorted_routs = sorted(routes, key=lambda x: x['final_amount'] / 100_000, reverse=True)
    for r in sorted_routs:
        profit = round(100 * (r["final_amount"] / 100_000 - 1), 2)
        if profit >= 1 or r["bank_init"] != 'Тинькофф':
            continue
        else:
            text = r["bank_init"] + ' -> ' + r['bch_coin'] + ' -> ' + r['binance_coin'] + ' -> ' + r['end_bank'] \
                   + '\n' + f'profit: *{profit} %*' + '\n\n' + f'Обменник: {r["exch_name"]}' + '\n\n' \
                   + f'‣Обмениваем на [bestchange]({r["href"]}): ' + '100 000 рублей ' + r[
                       'bank_init'] + '\n' + f'*по курсу {r["bch_rate"]}*\n' + 'получаем на binance: ' + f'{round(100_000 / r["bch_rate"], 3)}' + f' {r["bch_coin"]}\n' + '\n' \
                   + f'‣Продаем {r["bch_coin"]} на [binance spot]({r["binance_href"]}) ' + '\n*по курсу' + f' {round(r["binance_rate_spot"], 6)}*' + f'\nполучаем {round(r["middle_amount"], 3)} {r["binance_coin"]}' \
                   + f'\n\n‣Продаем {r["binance_coin"]}' + f' на [binance p2p]({r["binance_p2p_href"]}) \n*по курсу {r["binance_rate_p2p"]}*' \
                   + f'\nполучаем на {r["end_bank"]} {round(r["final_amount"], 3)}'
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
        if profit >= 1 or r["bank_init"] != 'Сбербанк':
            continue
        else:
            text = r["bank_init"] + ' -> ' + r['bch_coin'] + ' -> ' + r['binance_coin'] + ' -> ' + r['end_bank'] \
                   + '\n' + f'profit: *{profit} %*' + '\n\n' + f'Обменник: {r["exch_name"]}' + '\n\n' \
                   + f'‣Обмениваем на [bestchange]({r["href"]}): ' + '100 000 рублей ' + r[
                       'bank_init'] + '\n' + f'*по курсу {r["bch_rate"]}*\n' + 'получаем на binance: ' + f'{round(100_000 / r["bch_rate"], 3)}' + f' {r["bch_coin"]}\n' + '\n' \
                   + f'‣Продаем {r["bch_coin"]} на [binance spot]({r["binance_href"]}) \n*по курсу' + f' {round(r["binance_rate_spot"], 6)}*' + f'\nполучаем {round(r["middle_amount"], 3)} {r["binance_coin"]}' \
                   + f'\n\n‣Продаем {r["binance_coin"]} на [binance p2p]({r["binance_p2p_href"]}) \n*по курсу {r["binance_rate_p2p"]}*' \
                   + f'\nполучаем на {r["end_bank"]} {round(r["final_amount"], 3)}'
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
                   + '\n' + f'profit: *{profit} %*' + '\n\n' + f'Обменник: {r["exch_name"]}' + '\n\n' \
                   + f'‣Обмениваем на [bestchange]({r["href"]}): ' + '100 000 рублей ' + r[
                       'bank_init'] + '\n' + f'*по курсу {r["bch_rate"]}*\n' + 'Получаем на binance: ' + f'{round(100_000 / r["bch_rate"], 3)}' + f' {r["bch_coin"]}\n' + '\n' \
                   + f'‣Продаем {r["bch_coin"]} на [binance spot]({r["binance_href"]}) \n*по курсу' + f' {round(r["binance_rate_spot"], 6)}*' + f'\nполучаем {round(r["middle_amount"], 3)} {r["binance_coin"]}' \
                   + f'\n\n‣Продаем {r["binance_coin"]} на [binance p2p]({r["binance_p2p_href"]}) \n*по курсу {r["binance_rate_p2p"]}*' \
                   + f'\nполучаем на {r["end_bank"]} {round(r["final_amount"], 3)}'
            messages.append(text)
            max_messages -= 1
        if max_messages == 0:
            break
    return messages


async def start_sending():
    while True:
#        start = time.time()
        bestchange_data_banks, bestchange_data_usdt = get_bestchange_data()
#        end = time.time() - start
#        print('Bestchange download time: ', end)

#        start = time.time()
        (binance_spot_data, binance_coins), binance_p2p_data = get_binance_data()
#        end = time.time() - start
#       print('Binance download time: ', end)

#        start = time.time()
        garantex_data = get_garantex_data()
#        end = time.time() - start
#        print('Garantex download time: ', end)

#        start = time.time()
        routes_banks, routes_usdt, routes_bingar = find_paths(bestchange_data_banks, bestchange_data_usdt,
                                                              binance_spot_data,
                                                              binance_p2p_data, binance_coins, garantex_data)
#        end = time.time() - start
#        print('Filter time: ', end)

        coros = [send_to_vip(form_text_vip(routes_banks)),
                 send_to_sber_less_then_one(form_text_sber_less_then_one(routes_banks)),
                 send_to_tink_less_then_one(from_text_tink_less_then_one(routes_banks)),
                 send_to_no_bank(form_text_usdt(routes_usdt)),
                 send_to_binance_garantex(form_text_bingar(routes_bingar))]

#       start = time.time()
        await asyncio.gather(*coros)
#        end = time.time() - start
#       print('Send time: ', end)
        await asyncio.sleep(60)
#        print('___________________')


if __name__ == '__main__':
    asyncio.run(start_sending())
