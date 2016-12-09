# -*- coding: utf-8 -*-

import requests
import time
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class PublicAPI:
    def __init__(self, production=True, version="v1"):
        self.__host = production and "https://api.korbit.co.kr/%s/" % version \
                      or "https://api.korbit-test.com/%s/" % version

    # https://apidocs.korbit.co.kr/#public
    def ticker(self, currency_pair='btc_krw'):
        params = {
            'currency_pair': currency_pair
        }
        response = requests.get(urljoin(self.host, "ticker"), params=params)
        return response.json()

    def detailed_ticker(self, currency_pair='btc_krw'):
        params = {
            'currency_pair': currency_pair
        }
        response = requests.get(urljoin(self.host, "ticker/detailed"), params=params)
        print(response.url)
        return response.json()

    def orderbook(self, currency_pair='btc_krw', category="all", group=True):
        params = {
            'group': group,
            'category': category,
            'currency_pair': currency_pair
        }
        response = requests.get(urljoin(self.host, "orderbook"), params=params)
        return response.json()

    def bids_orderbook(self, currency_pair='btc_krw', group=True):
        return self.orderbook(currency_pair=currency_pair, category="bid", group=group)

    def asks_orderbook(self, currency_pair='btc_krw', group=True):
        return self.orderbook(currency_pair=currency_pair, category="ask", group=group)

    def list_of_filled_orders(self, currency_pair="btc_krw", interval="hour"):
        params = {
            'time': interval,
            'currency_pair': currency_pair
        }
        response = requests.get(urljoin(self.host, "transactions"), params=params)
        print(response.url)
        return response.json()

    def constants(self):
        response = requests.get(urljoin(self.host, "constants"))
        return response.json()

    @property
    def host(self):
        return self.__host

    @property
    def nonce(self):
        return int(time.time() * 1000)

    @property
    def nonce_params(self):
        return {
            'nonce': self.nonce
        }
