import json
import requests


class TreezClient:
    BASE_URL = 'https://api.treez.io/v2.0/dispensary/'

    def __init__(self, client_id, api_key, dispensary):
        self.client_id = client_id
        self.api_key = api_key
        self.dispensary = dispensary
        self.authorization_token = ''
        self.token_expiration = ''
        self._client = ''
        self.fetch_token()

    # def fetch_access_token(self):
    #     url = f'{self.BASE_URL}/{self.dispensary}/config/api/gettokens'
    #     headers = {
    #         'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #     payload_dict = {
    #         'client_id': self.client_id,
    #         'apikey': self.api_key
    #     }
    #     return self._client.post(url, headers=headers, data=payload_dict).json()['access_token']

    def fetch_products(self, page, last_updated_date='2020-01-01T00:00:00.000-00:00'):
        url = f'{self.BASE_URL}/{self.dispensary}/product/product_list/lastUpdated/after/{last_updated_date}'
        param_payload = {
            'active': 'true',
            'pagesize': 50,  # Max per page count
            'page': page  # Page will have to be iterated over in a range
        }
        return self._client.get(url, params=param_payload).json()

    def fetch_customers(self, page, last_updated_date='2020-01-01T00:00:00.000-00:00'):
        url = f'{self.BASE_URL}/{self.dispensary}/customer/lastUpdated/after/{last_updated_date}/page/{page}/pagesize/50'
        return self._client.get(url).json()

    def fetch_tickets(self, page, last_updated_date='2020-01-01T00:00:00.000-00:00'):
        url = f'{self.BASE_URL}/{self.dispensary}/ticket/lastUpdated/after/{last_updated_date}/page/{page}/pagesize/25'
        return self._client.get(url).json()

    def fetch_tickets_historical(self, page, closed_date):
        url = f'{self.BASE_URL}/{self.dispensary}/ticket/closedate/{closed_date}/page/{page}/pagesize/25'
        return self._client.get(url).json()

    def fetch_token(self):
        self._client = requests.Session()
        url = f'{self.BASE_URL}/{self.dispensary}/config/api/gettokens'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload_dict = {
            'client_id': self.client_id,
            'apikey': self.api_key
        }
        response = self._client.post(url, headers=headers, data=payload_dict).json()
        self.authorization_token = response['access_token']
        self.token_expiration = response ['expires_at']

        self._client.headers.update({
            'authorization': self.authorization_token,
            'client_id': self.client_id
        })

        return
