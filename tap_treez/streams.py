import singer
from datetime import datetime

from singer import bookmarks

LOGGER = singer.get_logger()

def set_latest_bookmark(current, compared):
    current_time = datetime.strptime(current.split('.')[0], "%Y-%m-%dT%H:%M:%S")
    compared_time = datetime.strptime(compared.split('.')[0], "%Y-%m-%dT%H:%M:%S")
    if compared_time >= current_time:
        formatted_time = str(compared_time) + '.000-07:00'
        return formatted_time.replace(' ', 'T')
    else:
        formatted_time = str(current_time) + '.000-07:00'
        return formatted_time.replace(' ', 'T')


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
            last_updated_at = '2000-01-01T00:00:00.000-00:00'
        
        new_bookmark = last_updated_at
        while response_length >= 50:
            response = self.client.fetch_products(
                page=current_page, last_updated_date=last_updated_at)
            
            products = response.get('data', {}).get('product_list', [])
            response_length = len(products)
            current_page += 1
            for product in products:
                new_bookmark = set_latest_bookmark(current=new_bookmark,
                                                   compared=product['last_updated_at'])
                singer.write_bookmark(self.state,
                                      self.tap_stream_id,
                                      self.replication_key,
                                      new_bookmark)
                yield product


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
            last_updated = '2000-01-01T00:00:00.000-00:00'
        new_bookmark = last_updated
        while response_length >= 50:
            response = self.client.fetch_customers(
                page=current_page, last_updated_date=last_updated)
            customers = response.get('data', [])
            response_length = len(customers)
            current_page += 1
            for customer in customers:
                new_bookmark = set_latest_bookmark(current=new_bookmark,
                                                   compared=customer['last_update'])
                singer.write_bookmark(self.state,
                                      self.tap_stream_id,
                                      self.replication_key,
                                      new_bookmark)
                yield customer


class TicketInfo(CatalogStream):
    tap_stream_id = 'tickets'
    key_properties = ['ticket_id']
    replication_key = 'last_updated_at'
    object_type = 'TICKET'

    def sync(self, **kwargs):
        response_length = 50
        current_page = 1
        last_updated_at = singer.get_bookmark(self.state,
                                                self.tap_stream_id,
                                                self.replication_key)
        if last_updated_at == None:
            last_updated_at = '2000-01-01T00:00:00.000-00:00'
        new_bookmark = last_updated_at
        while response_length >= 50:
            response = self.client.fetch_tickets(
                page=current_page, last_updated_date=last_updated_at)
            tickets = response.get('ticketList', [])
            response_length = len(tickets)
            current_page += 1
            for ticket in tickets:
                new_bookmark = set_latest_bookmark(current=new_bookmark,
                                                   compared=ticket['last_updated_at'])
                singer.write_bookmark(self.state,
                                      self.tap_stream_id,
                                      self.replication_key,
                                      new_bookmark)
                yield ticket

STREAMS = {
  'products': ProductInfo,
  'customers': CustomerInfo,
  'tickets': TicketInfo
}
