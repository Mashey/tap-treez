import pytest
import tap_treez.endpoints as endpoints


@pytest.mark.vcr(record_mode='new_episodes')
def test_product_endpoint():
  product_list = endpoints.get_products(test=True)
  product = product_list[0]

  assert isinstance(product_list, list)
  for product in product_list:
    assert 'product_id' in product
    assert 'product_status' in product
    assert 'last_updated_at' in product
    assert 'sellable_quantity' in product
    if len(product['sellable_quantity_detail']) > 0:
      for sellable_quantity_detail in product['sellable_quantity_detail']:
        assert 'inventory_type' in sellable_quantity_detail
        assert 'location' in sellable_quantity_detail
        assert 'sellable_quantity' in sellable_quantity_detail

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
    if len(product['lab_results']) > 0:
      for lab_results in product['lab_results']:
        assert 'result_type' in lab_results
        assert 'amount' in lab_results
        assert 'minimum_value' in lab_results
        assert 'maximum_value' in lab_results
        assert 'amount_type' in lab_results
        
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
  for ticket in ticket_list:
    assert 'type' in ticket
    assert 'ticket_id' in ticket
    assert 'order_number' in ticket
    assert 'external_order_number' in ticket
    assert 'order_source' in ticket
    assert 'created_by_employee' in ticket
    if ticket['created_by_employee'] != None:
      assert 'employee_id' in ticket['created_by_employee']
      assert 'name' in ticket['created_by_employee']
      assert 'role' in ticket['created_by_employee']
    
    assert 'customer_id' in ticket
    assert 'ticket_patient_type' in ticket
    assert 'cash_register_id' in ticket
    assert 'order_status' in ticket
    assert 'payment_status' in ticket
    assert 'date_created' in ticket
    assert 'last_updated_at' in ticket
    assert 'date_closed' in ticket
    assert 'post_tax_pricing' in ticket
    assert 'sub_total' in ticket
    assert 'tax_total' in ticket
    assert 'discount_total' in ticket
    assert 'total' in ticket
    assert 'ticket_note' in ticket
    assert 'refund_reason' in ticket
    assert 'original_ticket_id' in ticket
    assert 'delivery_address' in ticket
    if ticket['delivery_address'] != None:
      assert 'id' in ticket['delivery_address']
      assert 'street' in ticket['delivery_address']
      assert 'street2' in ticket['delivery_address']
      assert 'city' in ticket['delivery_address']
      assert 'county' in ticket['delivery_address']
      assert 'state' in ticket['delivery_address']
      assert 'zip' in ticket['delivery_address']

    assert 'scheduled_date' in ticket
    assert 'items' in ticket
    if len(ticket['items']) > 0:
      for item in ticket['items']:
        assert 'product_id' in item
        assert 'barcodes' in item
        assert 'inventory_barcodes' in item
        assert 'location_name' in item
        assert 'inventory_type' in item
        assert 'inventory_id' in item
        assert 'inventory_batch_id' in item
        assert 'size_id' in item
        assert 'product_size_name' in item
        assert 'product_type' in item
        assert 'product_brand' in item
        assert 'quantity' in item
        assert 'price_total' in item
        assert 'price_sell' in item
        assert 'product_unit' in item
        assert 'apply_automatic_discounts' in item
        assert 'POS_discounts' in item
        if len(item['POS_discounts']) > 0:
          for pos_discount in item['POS_discounts']:
            assert 'id' in pos_discount
            assert 'discount_title' in pos_discount
            assert 'discount_amount' in pos_discount
            assert 'discount_method' in pos_discount
            assert 'cart' in pos_discount

        assert 'discounts' in item
        if len(item['discounts']) > 0:
          for discount in item['discounts']:
            assert 'id' in discount
            assert 'discount_title' in discount
            assert 'discount_amount' in discount
            assert 'discount_method' in discount
            assert 'savings' in discount
            assert 'discount_category' in discount
            assert 'cart' in discount

        assert 'tax' in item
        if len(item['tax']) > 0:
          for tax in item['tax']:
            assert 'id' in tax
            assert 'rate'
            assert 'tax_name'
            assert 'amount'

        assert 'price_target' in item
        assert 'price_target_note' in item

    assert 'fees' in ticket
    assert 'payments' in ticket
    if len(ticket['payments']) > 0:
      for payment in ticket['payments']:
        assert 'payment_id' in payment
        assert 'payment_source' in payment
        assert 'payment_method' in payment
        assert 'amount_paid' in payment
        assert 'payment_date' in payment

    assert 'reward_eligible' in ticket
    assert 'reward_points_earned' in ticket
    assert 'reward_points_used' in ticket
    assert 'purchase_limit' in ticket
    assert 'employee_id' in ticket
    assert 'cash_drawer_name' in ticket
    assert 'delivery_route' in ticket


@pytest.mark.vcr(record_mode='new_episodes')
def test_customer_endpoint():
  customer_list = endpoints.get_customers(test=True)
  customer = customer_list[0]

  assert isinstance(customer_list, list)
  for customer in customer_list:
    assert 'status' in customer
    assert 'verification_status' in customer
    assert 'verification_reasons' in customer
    if len(customer['verification_reasons']) > 0:
      assert 'verification_reason' in customer['verification_reasons'][0]
      assert 'verification_reason_description' in customer['verification_reasons'][0]

    assert 'customer_id' in customer
    assert 'first_name' in customer
    assert 'middle_name' in customer
    assert 'nickname' in customer
    assert 'last_name' in customer
    assert 'birthday' in customer
    assert 'drivers_license' in customer
    assert 'drivers_license_expiration' in customer
    assert 'state_medical_id' in customer
    assert 'email' in customer
    assert 'phone' in customer
    assert 'notes' in customer
    assert 'permit_expiration' in customer
    assert 'physician_first_name' in customer
    assert 'physician_last_name' in customer
    assert 'physician_license' in customer
    assert 'physician_address' in customer
    assert 'physician_phone' in customer
    assert 'is_caregiver' in customer
    assert 'caregiver_license_number' in customer
    assert 'caregiver_name_1' in customer
    assert 'caregiver_name_2' in customer
    assert 'caregiver_details' in customer
    if len(customer['caregiver_details']) > 0:
      for caregiver in customer['caregiver_details']:
        assert 'caregiver_license_number' in caregiver
        assert 'caregiver_customer_id' in caregiver
        assert 'caregiver_name' in caregiver

    assert 'rewards_balance' in customer
    assert 'rewards_type' in customer
    assert 'signup_date' in customer
    assert 'last_visit_date' in customer
    assert 'last_update' in customer
    assert 'opt_out' in customer
    assert 'referral_source' in customer
    assert 'banned' in customer
    assert 'warning_1' in customer
    assert 'warning_2' in customer
    assert 'addresses' in customer
    if len(customer['addresses']) > 0:
      for address in customer['addresses']:
        assert 'type' in address
        assert 'street1' in address
        assert 'street2' in address
        assert 'city' in address
        assert 'state' in address
        assert 'zipcode' in address
        assert 'primary' in address

    assert 'merged_customer_ids' in customer
    assert 'merged_into_customer_id' in customer
    assert 'patient_type' in customer
    assert 'imageList' in customer
    if len(customer['imageList']) > 0:
      for image in customer['imageList']:
        assert 'type' in image
        assert 'url' in image
        assert 'lastupdated'

    assert 'customer_groups' in customer
