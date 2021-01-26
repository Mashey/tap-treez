import requests
import json
import tap_treez.service as service

client = service.create_session()
access_token = service.get_token()
dispensary = service.dispensary
headers = {
  'authorization': access_token,
  'client_id': service.client_id
}

def get_products():
  url = f'https://api.treez.io/v2.0/dispensary/{dispensary}/product/product_list'
  product_list = []
  page = 1
  response_count = 0

  param_payload = {
    'pagesize': 50, # Max per page count
    'page': page # Start at 1 and will iterate over each page
  }

  response = client.get(url, headers=headers, params=param_payload)
  json_response = response.json()

  # Clean this up into a secondary helper method perhaps
  while response_count < json_response['data']['total_count']:
    page += 1
    response_count += json_response['data']['page_count']
    product_list = product_list + (json_response['data']['product_list'])
    param_payload['page'] = page
    response = client.get(url, headers=headers, params=param_payload)
    json_response = response.json()

  

  return product_list




