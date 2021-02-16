import singer
from datetime import datetime
from .client import TreezClient

from singer import bookmarks
from singer import logger

LOGGER = singer.get_logger()


class Stream:
    tap_stream_id           = None
    key_properties          = []
    replication_method      = ''
    valid_replication_keys  = []
    replication_key         = ''
    object_type             = ''

    def __init__(self, client, state):
        self.client = client
        self.state = state

    def sync(self, *args, **kwargs):
        raise NotImplementedError("Sync of child class not implemented")

class CatalogStream(Stream):
    replication_method = 'INCREMENTAL'

class FullTableStream(Stream):
    replication_method = 'FULL_TABLE'

class ProductInfo(CatalogStream):
    tap_stream_id  = 'products'
    key_properties = ['product_id']
    replication_key = 'last_updated_at'
    object_type    = 'PRODUCT'

    def sync(self, **kwargs):
        response_length = 50
        current_page = 1
        last_updated_at = singer.get_bookmark(self.state,
                                              self.tap_stream_id,
                                              self.replication_key)
        if last_updated_at == None:
            last_updated_at = '2020-01-01T00:00:00.000-00:00'

        while response_length >= 50:
            response = self.client.fetch_products(
                page=current_page, last_updated_date=last_updated_at)
            
            if 'product_list' in response['data']:
                products = response['data']['product_list']
                response_length = len(products)
                current_page += 1
                for product in products:
                    yield product

            else:
                LOGGER.info('A new API Token is being fetched.')
                self.client.fetch_token()
                LOGGER.info(f'{response}')
                continue


class CustomerInfo(CatalogStream):
    tap_stream_id = 'customers'
    key_properties = ['customer_id']
    replication_key = 'last_update'
    object_type = 'CUSTOMER'

    def sync(self, **kwargs):
        response_length = 50
        current_page = 1
        last_updated = singer.get_bookmark(self.state,
                                                self.tap_stream_id,
                                                self.replication_key)
        if last_updated == None:
            last_updated = '2020-01-01T00:00:00.000-00:00'

        while response_length >= 50:
            response = self.client.fetch_customers(
                page=current_page, last_updated_date=last_updated)

            if 'data' in response:
                customers = response['data']
                response_length = len(customers)
                current_page += 1
                for customer in customers:
                    yield customer

            else:
                LOGGER.info('A new API Token is being fetched.')
                self.client.fetch_token()
                LOGGER.info(f'{response}')
                continue



class TicketInfo(CatalogStream):
    tap_stream_id = 'tickets'
    key_properties = ['ticket_id']
    replication_key = 'last_updated_at'
    object_type = 'TICKET'

    def sync(self, **kwargs):
        response_length = 25
        current_page = 1
        last_updated_at = singer.get_bookmark(self.state,
                                                self.tap_stream_id,
                                                self.replication_key)
        if last_updated_at == None:
            last_updated_at = '2020-01-01T00:00:00.000-00:00'

        while response_length >= 25:
            response = self.client.fetch_tickets(
                page=current_page, last_updated_date=last_updated_at)

            if 'ticketList' in response:
                tickets = response['ticketList']
                response_length = len(tickets)
                current_page += 1
                for ticket in tickets:
                    yield ticket

            else:
                LOGGER.info('A new API Token is being fetched.')
                self.client.fetch_token()
                LOGGER.info(f'{response}')
                continue


STREAMS = {
  'products': ProductInfo,
  'customers': CustomerInfo,
  'tickets': TicketInfo
}
