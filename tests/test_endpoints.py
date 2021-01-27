import pytest
import tap_treez.endpoints as endpoints


@pytest.mark.vcr(record_mode='new_episodes')
def test_product_endpoint():
  product_list = endpoints.get_products(test=True)
  product = product_list[0]

  assert isinstance(product_list, list)
  
  assert 'product_id' in product
  assert 'product_status' in product
  assert 'last_updated_at' in product
  assert 'sellable_quantity' in product
  if len(product['sellable_quantity_detail']) > 0:
    assert 'inventory_type' in product['sellable_quantity_detail'][0]
    assert 'location' in product['sellable_quantity_detail'][0]
    assert 'sellable_quantity' in product['sellable_quantity_detail'][0]

  assert 'category_type' in product
  assert 'product_configurable_fields' in product
  if len(product['product_configurable_fields']) > 0:
    assert 'name' in product['product_configurable_fields']
    # Different Product Types have different fields.  They will need to be accounted
    # for in the json schema files

  assert 'pricing' in product
  if len(product['pricing']) > 0:
    assert 'price_type' in product['pricing']
    assert 'price_sell' in product['pricing']
    assert 'tier_name' in product['pricing']

  assert 'attributes' in product
  if len(product['attributes']) > 0:
    assert 'general' in product['attributes']
    assert 'flavors' in product['attributes']
    assert 'effects' in product['attributes']
    assert 'ingredients' in product['attributes']
    assert 'internal_tags' in product['attributes']

  assert 'product_barcodes' in product
  assert 'e_commerce' in product
  if len(product['e_commerce']) > 0:
    assert 'all_images' in product['e_commerce']
    assert 'primary_image' in product['e_commerce']
    assert 'menu_title' in product['e_commerce']
    assert 'product_description' in product['e_commerce']
    assert 'minimum_visible_inventory_level' in product['e_commerce']
    assert 'hide_from_menu' in product['e_commerce']

  assert 'autoupdate_lab_results' in product
  assert 'lab_results' in product
  assert 'above_threshold' in product
  assert 'external_references' in product
  if len(product['external_references']) > 0:
    assert 'type' in product['external_references'][0]
    assert 'external_id' in product['external_references'][0]


@pytest.mark.vcr(record_mode='new_episodes')
def test_ticket_endpoint():
  ticket_list = endpoints.get_tickets(test=True)
  ticket = ticket_list[0]

  assert isinstance(ticket_list, list)
  


@pytest.mark.vcr(record_mode='new_episodes')
def test_customer_endpoint():
  customer_list = endpoints.get_customers(test=True)

  assert isinstance(customer_list, list)
  assert(len(customer_list) == 100)
