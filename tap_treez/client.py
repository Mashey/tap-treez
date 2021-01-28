import json
import requests

class TreezClient:
  BASE_URL = 'https://api.treez.io/v2.0/dispensary/'

  def __init__(self, client_id, api_key, dispensary):
    self.dispensary = dispensary
    self._client = requests.Session()
    self.access_token = self.fetch_access_token(client_id, api_key)
    self._client.headers.update({
      'authorization': self.access_token,
      'client_id': client_id
    })

  def fetch_access_token(self, client_id, api_key):
    url = f'{self.BASE_URL}/{self.dispensary}/config/api/gettokens'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload_dict = {
        'client_id': client_id,
        'apikey': api_key
    }
    return self._client.post(url, headers=headers, data=payload_dict).json()['access_token']

  def fetch_products(self, page):
    url = f'{self.BASE_URL}/{self.dispensary}/product/product_list'
    param_payload = {
        'active': 'true',
        'pagesize': 50,  # Max per page count
        'page': page  # Page will have to be iterated over in a range
    }
    return self._client.get(url, params=param_payload).json()

  def fetch_customers(self, page, last_updated_date='2019-09-18T11:11:36.000-07:00'):
    url = f'{self.BASE_URL}/{self.dispensary}/customer/lastUpdated/after/{last_updated_date}/page/{page}/pagesize/50'
    return self._client.get(url).json()

  def fetch_tickets(self, page, last_updated_date='2019-09-18T11:11:36.000-07:00'):
    url = f'{self.BASE_URL}/{self.dispensary}/ticket/lastUpdated/after/{last_updated_date}/page/{page}/pagesize/50'
    return self._client.get(url).json()
