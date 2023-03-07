"""
Файл с парсингом данных с Garantex
"""
from pprint import pprint

import requests
import base64
import time
import datetime
import random
import jwt
from pasrsers.api_keys import GARANTEX_SECRET, GARANTEX_UID


def generate_new_jwt():
    private_key = GARANTEX_SECRET
    uid = GARANTEX_UID
    host = 'garantex.io'  # для тестового сервера используйте stage.garantex.biz

    key = base64.b64decode(private_key)
    iat = int(time.mktime(datetime.datetime.now().timetuple()))

    claims = {
        "exp": iat + 1 * 60 * 60,  # JWT Request TTL in seconds since epoch
        "jti": hex(random.getrandbits(12)).upper()
    }

    jwt_token = jwt.encode(claims, key, algorithm="RS256")

    # print("JWT request token: %s\n" % jwt_token)

    ret = requests.post('https://dauth.' + host + '/api/v1/sessions/generate_jwt',
                        json={'kid': uid, 'jwt_token': jwt_token})


def get_garantex_data():
    """
    Возвращает данные об garantex
    :return:
    """
    try:
        markets = list(map(lambda x: x['id'], requests.get('https://garantex.io/api/v2/markets').json()))
    except requests.exceptions.JSONDecodeError:
        generate_new_jwt()
        markets = list(map(lambda x: x['id'], requests.get('https://garantex.io/api/v2/markets').json()))
    garantex_data = {}
    for m in markets:
        r = requests.get('https://garantex.io/api/v2/depth', params={'market': m})
        garantex_data[m] = {'market': m,
                            'asks_price': r.json()['asks'][0]['price'],
                            'bids_price': r.json()['bids'][0]['price'],
                            'href': f'https://garantex.io/trading/{m}'}

    return garantex_data


if __name__ == '__main__':
    pass
    # import base64
    # import time
    # import datetime
    # import random
    # import requests
    # import jwt
    #
    # private_key = GARANTEX_SECRET
    # uid = GARANTEX_UID
    # host = 'garantex.io'  # для тестового сервера используйте stage.garantex.biz

    # key = base64.b64decode(private_key)
    # iat = int(time.mktime(datetime.datetime.now().timetuple()))

    # claims = {
    #     "exp": iat + 1 * 60 * 60,  # JWT Request TTL in seconds since epoch
    #     "jti": hex(random.getrandbits(12)).upper()
    # }
    #
    # jwt_token = jwt.encode(claims, key, algorithm="RS256")

    # print("JWT request token: %s\n" % jwt_token)

    # ret = requests.post('https://dauth.' + host + '/api/v1/sessions/generate_jwt',
    #                     json={'kid': uid, 'jwt_token': jwt_token})

    # print("JWT response code: %d" % ret.status_code)
    # print("JWY response text: %s\n" % ret.text)

    # token = ret.json().get('token')

    # print("JWT token: %s\n" % token)

    # r = requests.get('https://garantex.io/api/v2/markets')
    # r = requests.get('https://garantex.io/api/v2/depth', params={'market': 'btcrub'})
    # r = requests.get('https://garantex.io/api/v2/depth', params={'market': 'btcrub'})
    # pprint(get_garantex_data())
    # print(r.json()['asks'][0]['price'], r.json()['bids'][0]['price'])
