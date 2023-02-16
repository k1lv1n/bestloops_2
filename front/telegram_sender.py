"""
Файл с функциями отправки сообщений по каналам. Скорее всего в итоге он будет иметь другой вид.
"""
from aiogram import Bot, types, Dispatcher, executor
from configs import BOT_TOKEN, TEST_CHANNEL_ID
import asyncio

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def send_to_sber_less_then_one(data_to_be_sent):
    pass


def send_to_tink_less_then_one(data_to_be_sent):
    pass


def send_to_vip(data_to_be_sent):
    pass


def send_to_qiwi(data_to_be_sent):
    pass


def send_to_binance_garantex(data_to_be_sent):
    pass


async def send_to_no_bank(data_to_be_sent):
    await bot.send_message(chat_id=TEST_CHANNEL_ID, text=data_to_be_sent)


async def send_to_test(data_to_be_sent):
    await bot.send_message(chat_id=TEST_CHANNEL_ID, text=data_to_be_sent)


async def start_sending():
    while True:
        data = {'no_bank': 'no_bank', 'test': 'test_bank'}
        coros = [send_to_test(data['test']), send_to_no_bank(data['no_bank'])]
        await asyncio.gather(*coros)
        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(start_sending())
