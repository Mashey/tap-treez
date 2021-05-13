import singer
from datetime import datetime, timedelta
from .client import TreezClient

from singer import bookmarks
from singer import logger
from ratelimit import limits, sleep_and_retry

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

    @sleep_and_retry
    @limits(calls=5, period=2)
    def sync(self, **kwargs):
        product_count = 0
        response_length = 50
        current_page = 1
        last_updated_at = singer.get_bookmark(self.state,
                                              self.tap_stream_id,
                                              self.replication_key)
        if last_updated_at == None:
            last_updated_at = datetime.strftime(
                datetime.now(), "%Y-%m-%dT00:00:00.000Z")

        while response_length >= 50:
            response = self.client.fetch_products(
                page=current_page, last_updated_date=last_updated_at)
            
            if 'product_list' in response['data']:
                LOGGER.info(f'Products written: {product_count}')
                products = response['data']['product_list']
                response_length = len(products)
                current_page += 1
                for product in products:
                    product_count += 1
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

    @sleep_and_retry
    @limits(calls=4, period=2)
    def sync(self, **kwargs):
        customer_count = 0
        response_length = 50
        current_page = 1
        last_updated = singer.get_bookmark(self.state,
                                                self.tap_stream_id,
                                                self.replication_key)
        if last_updated == None:
            last_updated = datetime.strftime(
                datetime.now(), "%Y-%m-%dT00:00:00.000Z")

        while response_length >= 50:
            response = self.client.fetch_customers(
                page=current_page, last_updated_date=last_updated)

            LOGGER.info(f'{response.keys()}')
            if 'data' in response:
                LOGGER.info(f'Customers written: {customer_count}')
                customers = response['data']
                response_length = len(customers)
                current_page += 1
                for customer in customers:
                    customer_count += 1
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

    @sleep_and_retry
    @limits(calls=4, period=2)
    def sync(self, **kwargs):
        response_length = 25
        current_page = 1
        last_updated_at = singer.get_bookmark(self.state,
                                                self.tap_stream_id,
                                                self.replication_key)
        if last_updated_at == None:
            last_updated_at = datetime.strftime(
                datetime.now(), "%Y-%m-%dT00:00:00.000Z")

        while response_length >= 25:
            response = self.client.fetch_tickets(
                page=current_page, last_updated_date=last_updated_at)

            if 'ticketList' in response:
                tickets = response['ticketList']
                response_length = len(tickets)
                current_page += 1
                for ticket in tickets:
                    singer.write_bookmark(self.state,
                                          self.tap_stream_id,
                                          self.replication_key,
                                          ticket['last_updated_at'])
                    singer.write_state(self.state)
                    yield ticket

            else:
                LOGGER.info('A new API Token is being fetched.')
                self.client.fetch_token()
                LOGGER.info(f'{response}')
                continue

# The class below was used to do a backfill.  Because the API ordered the last
# updated tickets from newest to olded - trying to iterate in reverse while new
# tickets were coming in caused duplicates frequently.  So for backfill the closed
# at end point was used.

# class TicketHistorical(FullTableStream):
#     tap_stream_id = 'tickets'
#     key_properties = ['ticket_id']
#     replication_key = 'date_closed'
#     object_type = 'TICKET'

#     @sleep_and_retry
#     @limits(calls=4, period=2)
#     def sync(self, **kwargs):

#         # last_date_ran = singer.get_bookmark(self.state,
#         #                                     self.tap_stream_id,
#         #                                     self.replication_key)

#         # Change the last_date_ran to 2017-07-01 and
#         # in the while loop to stop at 2020-12-31

#         # if last_date_ran == None:
#         last_date_ran = '2021-02-15'

#         LOGGER.info(f'Starting date: {last_date_ran}')
#         while last_date_ran != '2021-03-04':
#             # Go through all the pages for each date
#             tickets_this_day = 0
#             response_length = 25
#             current_page = 1

#             while response_length >= 25:
#                 response = self.client.fetch_tickets_historical(page=current_page,
#                                                                 closed_date=last_date_ran)

#                 if 'ticketList' in response:
#                     LOGGER.info(f'Tickets for {last_date_ran} written: {tickets_this_day}')
#                     tickets = response['ticketList']
#                     response_length = len(tickets)
#                     current_page += 1
#                     for ticket in tickets:
#                         tickets_this_day += 1
#                         yield ticket

#                 else:
#                     LOGGER.info('A new API Token is being fetched.')
#                     self.client.fetch_token()
#                     LOGGER.info(f'{response}')
#                     continue

#             # Now add a date to the last_date_run to get the next day
#             last_date_ran = datetime.strftime((datetime.strptime(last_date_ran, "%Y-%m-%d") + timedelta(days=1)),
#                                               "%Y-%m-%d")
#             LOGGER.info(f'Next Date is {last_date_ran}')
#             singer.write_bookmark(self.state,
#                                   self.tap_stream_id,
#                                   self.replication_key,
#                                   last_date_ran)
#             singer.write_state(self.state)


STREAMS = {
  'products': ProductInfo,
#   'customers': CustomerInfo,
  'tickets': TicketInfo
#   'tickets': TicketHistorical
}
