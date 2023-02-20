"""
Файл с парсингом данных с BestChange
"""
import re
from pprint import pprint

сбер = 42
тинь = 105
райф = 157


def get_bestchange_data():
    """
    Возвращает данные об обменниках
    :return:
    """

    from bestchange_api import BestChange

    bitcoin_bep20_id = 43
    CRYPTO_IDS = [2, 8, 10, 16, 19, 23, 24, 26, 32, 36, 48, 61, 73, 82, 93, 99, 104, 110,
                  115, 124, 133, 134, 135, 138, 139, 140, 149, 160, 161, 162, 163, 168,
                  172, 173, 175, 177, 178, 180, 181, 182, 185, 189, 197, 198, 201, 202,
                  203, 205, 206, 208, 210, 212, 213, 216, 217, 218, 227, 228, 235]
    sber = 42
    tink = 105
    raif = 157
    qiwi = 63
    usdt = 10
    banks = {42: 'sber', 105: 'tinkoff', 157: 'raifaizen', 63: 'qiwi'}
    BINANCE_COINS = {'1INCH', '1INCHDOWN', '1INCHUP', 'AAVE', 'AAVEDOWN', 'AAVEUP', 'ACA', 'ACH', 'ACM', 'ADA',
                     'ADADOWN', 'ADAUP', 'ADX', 'AED', 'AERGO', 'AFN', 'AGIX', 'AGLD', 'AION', 'AKRO', 'ALCX', 'ALGO',
                     'ALICE', 'ALPACA', 'ALPHA', 'ALPINE', 'AMB', 'AMD', 'AMP', 'ANC', 'ANKR', 'ANT', 'APE', 'API3',
                     'APT', 'AR', 'ARDR', 'ARK', 'ARPA', 'ARS',
                     'ASR', 'AST', 'ASTR', 'ATA', 'ATM', 'ATOM', 'AUCTION', 'AUD', 'AUDIO', 'AUTO', 'AVA', 'AVAX',
                     'AXS', 'BADGER', 'BAKE', 'BAL', 'BAND', 'BAR', 'BAT', 'BCH', 'BCHA', 'BCHDOWN', 'BCHUP', 'BCX',
                     'BDOT', 'BEAM', 'BEL', 'BETA', 'BETH', 'BGBP', 'BGN', 'BHD', 'BICO', 'BIDR', 'BIFI', 'BLZ', 'BNB',
                     'BNBDOWN', 'BNBUP', 'BNC', 'BND', 'BNT', 'BNX', 'BOND', 'BRL', 'BSW', 'BTC',
                     'BTCDOWN', 'BTCST', 'BTCUP', 'BTG', 'BTS', 'BTTC', 'BTTOLD', 'BURGER', 'BUSD', 'BYN', 'C98', 'CAD',
                     'CAKE', 'CAN', 'CELO', 'CELR', 'CFX', 'CHESS', 'CHF', 'CHR', 'CHZ', 'CITY', 'CKB', 'CLP', 'CLV',
                     'COCOS',
                     'COMP', 'COP', 'COS', 'COTI', 'CREAM', 'CRV', 'CTK', 'CTSI', 'CTXC', 'CVC', 'CVP', 'CVX', 'CZK',
                     'DAI', 'DAR', 'DASH', 'DATA', 'DCR', 'DEGO', 'DENT', 'DEXE', 'DF', 'DGB', 'DIA', 'DKK', 'DOCK',
                     'DODO', 'DOGE', 'DOP', 'DOT', 'DOTDOWN', 'DOTUP', 'DREP', 'DUSK', 'DYDX', 'DZD', 'EFI', 'EGLD',
                     'EGP', 'ELF', 'ELON', 'ENJ', 'ENS', 'EOS', 'EOSDOWN', 'EOSUP', 'EPS', 'EPX', 'ERN', 'ETB', 'ETC',
                     'ETH', 'ETHDOWN', 'ETHUP', 'ETHW', 'EUR', 'EVX', 'FARM', 'FET', 'FIDA', 'FIL', 'FILDOWN', 'FILUP',
                     'FIO', 'FIRO',
                     'FIS', 'FLM', 'FLOW', 'FLR', 'FLUX', 'FOR', 'FORTH', 'FRONT', 'FTM', 'FTT', 'FUN', 'FXS', 'GAL',
                     'GALA', 'GAS', 'GBP', 'GEL', 'GFT', 'GHS', 'GHST', 'GLM', 'GLMR', 'GMT', 'GMX', 'GNO', 'GNS',
                     'GRT', 'GRTDOWN', 'GRTUP', 'GTC', 'GYEN', 'HARD', 'HBAR', 'HFT', 'HIFI', 'HIGH', 'HIVE', 'HKD',
                     'HNT', 'HOOK', 'HOT', 'HRK', 'HUF', 'ICP', 'ICX', 'IDEX', 'IDR', 'IDRT', 'ILV', 'IMX', 'INJ',
                     'INR', 'IOST', 'IOTA', 'IOTX', 'IQ', 'IRIS', 'JASMY', 'JEX', 'JOD', 'JOE', 'JPY', 'JST', 'JUV',
                     'KAVA', 'KDA', 'KES', 'KEY', 'KEYFI', 'KGS', 'KHR', 'KLAY', 'KMD', 'KNC', 'KP3R', 'KSM', 'KWD',
                     'KZT', 'LAK', 'LAZIO', 'LBA', 'LDO', 'LEVER', 'LINA', 'LINK', 'LINKDOWN', 'LINKUP', 'LIT', 'LOKA',
                     'LOOKS', 'LOOM',
                     'LPT', 'LRC', 'LSK', 'LTC', 'LTCDOWN', 'LTCUP', 'LTO', 'LUNA', 'LUNC', 'LYD', 'MA', 'MAGIC',
                     'MANA', 'MASK', 'MATIC', 'MBL', 'MBOX', 'MC', 'MDT', 'MDX', 'MINA', 'MIR', 'MITH', 'MKR',
                     'MLN', 'MMK', 'MNT', 'MOB', 'MOVR', 'MTL', 'MTLX', 'MULTI', 'MXN', 'NEAR', 'NEBL',
                     'NEO', 'NEXO', 'NFT', 'NGN', 'NKN', 'NMR', 'NOK', 'NULS', 'NVT', 'NZD', 'OAX', 'OCEAN', 'OG',
                     'OGN', 'OM', 'OMG', 'OMR', 'ONE', 'ONG', 'ONT', 'OOKI', 'OP', 'ORN', 'OSMO', 'OXT', 'PARA', 'PAX',
                     'PAXG', 'PEN', 'PEOPLE', 'PERL', 'PERP', 'PGALA', 'PHA', 'PHB', 'PHP', 'PIVX', 'PKR', 'PLA', 'PLN',
                     'PNT', 'POLS', 'POLYX', 'POND', 'PORTO', 'POWR', 'PROM', 'PROS', 'PSG', 'PUNDIX', 'PYR', 'QAR',
                     'QI', 'QKC', 'QLC', 'QNT', 'QTUM', 'QUICK', 'RAD',
                     'RARE', 'RAY', 'REEF', 'REI', 'REN', 'REP', 'REQ', 'RIF', 'RLC', 'RNDR', 'RON', 'ROSE',
                     'RPL', 'RSR', 'RUB', 'RUNE', 'RVN', 'SAND', 'SANTOS', 'SAR', 'SBTC', 'SC', 'SCRT', 'SDG', 'SEK',
                     'SFP', 'SHIB', 'SKL', 'SLP', 'SNM', 'SNT', 'SNX', 'SOL', 'SOLO', 'SPELL', 'SRM', 'SSV', 'STEEM',
                     'STG', 'STMX', 'STORJ', 'STPT', 'STRAX', 'STX', 'SUN',
                     'SUPER', 'SUSHI', 'SUSHIDOWN', 'SUSHIUP', 'SXP', 'SXPDOWN', 'SXPUP', 'SYS', 'T', 'TCT', 'TFUEL',
                     'THETA', 'TJS', 'TKO', 'TLM', 'TMT', 'TND', 'TOMO', 'TORN', 'TRB', 'TRIBE', 'TROY',
                     'TRU', 'TRX', 'TRXDOWN', 'TRXUP', 'TRY', 'TUSD', 'TVK', 'TWD', 'TWT', 'TZS', 'UAH', 'UFT', 'UGX',
                     'UMA', 'UNFI', 'UNI', 'UNIDOWN', 'UNIUP', 'USD', 'USDC', 'USDP', 'USDT', 'USTC', 'UTK', 'UYU',
                     'UZS', 'VAI', 'VET', 'VGX', 'VIB', 'VIDT', 'VITE', 'VND', 'VOXEL', 'VRT', 'VTHO', 'WABI', 'WAN',
                     'WAVES', 'WAXP', 'WBNB', 'WBTC', 'WETH', 'WIN',
                     'WING', 'WNXM', 'WOO', 'WRX', 'WSOL', 'WTC', 'XAF',
                     'XEC', 'XEM', 'XLM', 'XLMDOWN', 'XLMUP', 'XMR', 'XNO', 'XOF', 'XRP', 'XRPDOWN', 'XRPUP', 'XTZ',
                     'XTZDOWN', 'XTZUP', 'XVG', 'XVS', 'YFI', 'YFIDOWN', 'YFII', 'YFIUP', 'YGG', 'ZAR', 'ZEC', 'ZEN',
                     'ZIL', 'ZRX'}

    api = BestChange()
    currencies = api.currencies().get()
    exchangers = api.exchangers().get()
    bch_prices_banks = []

    # pprint(currencies)
    # print(decode_BCH_ticker('Cosmos (ATOM)'))
    for bank_id in [sber, tink, raif, qiwi]:
        for cr_id in CRYPTO_IDS:
            res = api.rates().filter(bank_id, cr_id)
            bch_prices_banks.append(
                {'bank': banks[bank_id], 'coin': decode_BCH_ticker(currencies[cr_id]['name']), 'rate': res[0]['rate'],
                 'exchangers': exchangers[res[0]['exchange_id']]['name'],
                 'href': f'https://www.bestchange.ru/index.php?from={bank_id}&to={cr_id}'
                 })
        res = api.rates().filter(bank_id, bitcoin_bep20_id)
        bch_prices_banks.append({'bank': banks[bank_id], 'coin': 'BTC', 'rate': res[0]['rate'],
                                 'exchangers': exchangers[res[0]['exchange_id']]['name'],
                                 'href': f'https://www.bestchange.ru/index.php?from={bank_id}&to={93}'})
    bch_prices_usdt = []
    for bank_id in [usdt]:
        CRYPTO_IDS.pop(10)
        for cr_id in CRYPTO_IDS:
            res = api.rates().filter(bank_id, cr_id)
            bch_prices_usdt.append(
                {'bank': 'usdt', 'coin': decode_BCH_ticker(currencies[cr_id]['name']), 'rate': res[0]['rate'],
                 'exchangers': exchangers[res[0]['exchange_id']]['name'],
                 'href': f'https://www.bestchange.ru/index.php?from={bank_id}&to={cr_id}'})
        res = api.rates().filter(bank_id, bitcoin_bep20_id)
        bch_prices_usdt.append({'bank': 'usdt', 'coin': 'BTC', 'rate': res[0]['rate'],
                                'exchangers': exchangers[res[0]['exchange_id']]['name'],
                                'href': f'https://www.bestchange.ru/index.php?from={bank_id}&to={93}'})

    return bch_prices_banks, bch_prices_usdt


def decode_BCH_ticker(ticker):
    m = re.search('\((.+?)\)', ticker)
    if m:
        return m.group(1)
    return ticker


if __name__ == '__main__':
    pprint(get_bestchange_data())
