from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

api_key = os.getenv('APIKey')
client_id = os.getenv('Client_Id')
dispensary = os.getenv('Dispensary')

def create_session():
  return requests.Session()

def get_token():
  url = f"https://api.treez.io/v2.0/dispensary/{dispensary}/config/api/gettokens"
  client = create_session()

  headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
  }

  payload_dict = {
    'client_id': client_id,
    'apikey': api_key
  }

  response = client.post(url, headers=headers, data=payload_dict)
  token = response.json()['access_token']

  return token

