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

## Singer Bookmark for date
last_ticket_date = '2019-09-18T14%3A51%3A27.000-07%3A00'
last_customer_date = '2019-09-18T14%3A51%3A27.000-07%3A00'

def get_products(test=False):
  url = f'https://api.treez.io/v2.0/dispensary/{dispensary}/product/product_list'
  product_list = []
  page = 1
  response_count = 0

  param_payload = {
    'active': 'true',
    'pagesize': 50, # Max per page count
    'page': page # Start at 1 and will iterate over each page
  }

  response = client.get(url, headers=headers, params=param_payload)
  json_response = response.json()

  # Clean this up into a secondary helper method perhaps
  while response_count < json_response['data']['total_count']:
    page += 1
    if page == 6 and test == True:
      return product_list
    response_count += json_response['data']['page_count']
    product_list += json_response['data']['product_list']
    param_payload['page'] = page
    response = client.get(url, headers=headers, params=param_payload)
    json_response = response.json()

  

  return product_list


def get_tickets(test=False):
  ticket_list = []
  page = 1
  url = f'https://api.treez.io/v2.0/dispensary/{dispensary}/ticket/lastUpdated/after/{last_ticket_date}/page/{page}/pagesize/50'

  response = client.get(url, headers=headers)
  json_response = response.json()

  while json_response['ticketList'] != []:
    page += 1
    if page == 6 and test == True:
      return ticket_list
    ticket_list += json_response['ticketList']
    url = f'https://api.treez.io/v2.0/dispensary/{dispensary}/ticket/lastUpdated/after/{last_ticket_date}/page/{page}/pagesize/50'
    response = client.get(url, headers=headers)
    json_response = response.json()

  # The Ticket API returns tickets newest first.  The initial run will collect a lot of data
  # but after that the singer tap will only pull things after a certain date in the bookmarks.
  # The bookmark will need to be updated with the first elements updated at value
  # last_ticket_date = ticket_list[0]['last_update_at']

  return ticket_list


def get_customers(test=False):
  customer_list = []
  page = 1
  url = f'https://api.treez.io/v2.0/dispensary/{dispensary}/customer/lastUpdated/after/{last_customer_date}/page/{page}/pagesize/50'

  response = client.get(url, headers=headers)
  json_response = response.json()

  while json_response['data'] != []:
    page += 1
    if page == 6 and test == True:
      return customer_list
    customer_list += json_response['data']
    url = f'https://api.treez.io/v2.0/dispensary/{dispensary}/customer/lastUpdated/after/{last_customer_date}/page/{page}/pagesize/50'
    response = client.get(url, headers=headers)
    json_response = response.json()

  # The Customer API returns tickets newest first.  The initial run will collect a lot of data
  # but after that the singer tap will only pull things after a certain date in the bookmarks.
  # The bookmark will need to be updated with the first elements updated at value
  # last_customer_date = customer_list[0]['last_update']

  return customer_list
