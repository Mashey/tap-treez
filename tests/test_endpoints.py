import pytest
import tap_treez.endpoints as endpoints


@pytest.mark.vcr(record_mode='new_episodes')
def test_product_endpoint():
  product_list = endpoints.get_products(test=True)

  assert isinstance(product_list, list)
  assert(len(product_list), 200)

@pytest.mark.vcr(record_mode='new_episodes')
def test_ticket_endpoint():
  ticket_list = endpoints.get_tickets(test=True)

  assert isinstance(ticket_list, list)
  assert(len(ticket_list) == 200)


@pytest.mark.vcr(record_mode='new_episodes')
def test_customer_endpoint():
  customer_list = endpoints.get_customers(test=True)

  assert isinstance(customer_list, list)
  assert(len(customer_list) == 200)
