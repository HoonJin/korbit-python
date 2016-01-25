#-*- coding: utf-8 -*-

from .public_api import PublicAPI
import requests
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class PrivateAPI(PublicAPI):
    def __init__(self, client_id, secret, production=True, version="v1"):
        super(self.__class__, self).__init__(production, version)
        self.__client_id = client_id
        self.__secret = secret
        self.__token = {}

    # https://apidocs.korbit.co.kr/#authentication
    def create_token_directly(self, username, password):
        payload = {
            'client_id': self.__client_id,
            'client_secret': self.__secret,
            'username': username,
            'password': password,
            'grant_type': "password"
        }
        response = requests.post(urljoin(self.host, "oauth2/access_token"), data=payload)

        self.__token = response.json()
        return self.__token

    def refresh_token(self):
        payload = {
            'client_id': self.__client_id,
            'client_secret': self.__secret,
            'refresh_token': self.__token['refresh_token'],
            'grant_type': "refresh_token"
        }
        response = requests.post(urljoin(self.host, "oauth2/access_token"), data=payload)

        self.__token = response.json()
        return self.__token

    def get_user_info(self):
        response = requests.get(urljoin(self.host, "user/info"), params=self.nonce_params, headers=self.headers)
        return response.json()

    @property
    def headers(self):
        return {
            'Accept': 'application/json',
            'Authorization': "%s %s" % (self.__token['token_type'], self.__token['access_token'])
        }

    # https://apidocs.korbit.co.kr/#exchange
    def bid_order(self, bid_type, coin_amount=0, price=0, fiat_amount=0):
        payload = {
            'type': bid_type,
            'price': price,
            'coin_amount': coin_amount,
            'fiat_amount': fiat_amount,
            'nonce': self.nonce
        }
        response = requests.post(urljoin(self.host, "user/orders/buy"), data=payload, headers=self.headers)
        return response.json()

    def market_bid_order(self, fiat_amount):
        return self.bid_order('market', fiat_amount=fiat_amount)

    def limit_bid_order(self, coin_amount, price):
        return self.bid_order('limit', coin_amount=coin_amount, price=price)

    def ask_order(self, ask_type, coin_amount, price=0):
        payload = {
            'type': ask_type,
            'price': price,
            'coin_amount': coin_amount,
            'nonce': self.nonce
        }
        response = requests.post(urljoin(self.host, "user/orders/sell"), data=payload, headers=self.headers)
        return response.json()

    def market_ask_order(self, coin_amount):
        return self.ask_order('market', coin_amount)

    def limit_ask_order(self, coin_amount, price):
        return self.ask_order('limit', coin_amount, price)

    def cancel_order(self, ids):
        payload = {
            'id': ids,
            'nonce': self.nonce
        }
        response = requests.post(urljoin(self.host, "user/orders/cancel"), data=payload, headers=self.headers)
        return response.json()

    def list_open_orders(self, offset=0, limit=10):
        params = {
            'offset': offset,
            'limit': limit,
            'nonce': self.nonce
        }
        response = requests.get(urljoin(self.host, "user/orders/open"), params=params, headers=self.headers)
        return response.json()

    def transaction_history(self, category="", offset=0, limit=10, order_id=0):
        # TODO: make use custom parameter
        response = requests.get(urljoin(self.host, "user/transactions"), params=self.nonce_params, headers=self.headers)
        return response.json()

    # https://apidocs.korbit.co.kr/#fiat
    def assign_virtual_bank_account(self, currency="krw"):
        payload = {
            'currency': currency,
            'nonce': self.nonce
        }
        response = requests.post(urljoin(self.host, "user/fiats/address/assign"), data=payload, headers=self.headers)
        return response.json()

    def register_user_bank_account(self, bank, account, currency="krw"):
        # https://s3.amazonaws.com/korbit.api/bank-names-ko-1.0.0.json
        payload = {
            'currency': currency,
            'bank': bank,
            'account': account,
            'nonce': self.nonce
        }
        response = requests.post(urljoin(self.host, "user/fiats/address/register"), data=payload, headers=self.headers)
        return response.json()

    def request_withdrawal(self, amount, currency="krw"):
        payload = {
            'currency': currency,
            'amount': amount,
            'nonce': self.nonce
        }
        response = requests.post(urljoin(self.host, "user/fiats/out"), data=payload, headers=self.headers)
        return response.json()

    def state_of_withdrawal_requests(self, currency="krw"):
        params = {
            'currency': currency,
            'nonce': self.nonce
        }
        response = requests.get(urljoin(self.host, "user/fiats/status"), params=params, headers=self.headers)
        return response.json()

    def cancel_withdrawal_request(self, fiat_out_id, currency="krw"):
        payload = {
            'currency': currency,
            'id': fiat_out_id,
            'nonce': self.nonce
        }
        response = requests.post(urljoin(self.host, "user/fiats/out/cancel"), data=payload, headers=self.headers)
        return response.json()

    # https://apidocs.korbit.co.kr/#wallet
    def retrieve_wallet_status(self):
        response = requests.get(urljoin(self.host, "user/wallet"), params=self.nonce_params, headers=self.headers)
        return response.json()

    def assign_btc_address(self, currency="btc"):
        payload = {
            'currency': currency,
            'nonce': self.nonce
        }
        response = requests.post(urljoin(self.host, "user/coins/address/assign"), data=payload, headers=self.headers)
        return response.json()

    def request_btc_withdrawal(self, address, amount, currency="btc"):
        payload = {
            'address': address,
            'amount': amount,
            'currency': currency,
            'nonce': self.nonce
        }
        response = requests.post(urljoin(self.host, "user/coins/out"), data=payload, headers=self.headers)
        return response.json()

    def status_of_btc_deposit_and_transfer(self, id="", currency="btc"):
        params = {
            'currency': currency,
            'nonce': self.nonce
        }
        if id != "":
            params['id'] = id
        response = requests.get(urljoin(self.host, "user/coins/status"), params=params, headers=self.headers)
        return response.json()

    def cancel_btc_transfer_request(self, id, currency="btc"):
        payload = {
            'id': id,
            'currency': currency,
            'nonce': self.nonce
        }
        response = requests.post(urljoin(self.host, "user/coins/out/cancel"), data=payload, headers=self.headers)
        return response.json()
