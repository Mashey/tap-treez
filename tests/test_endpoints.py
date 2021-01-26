import pytest
import tap_treez.endpoints as endpoints


@pytest.mark.vcr(record_mode='new_episodes')
def test_product_endpoint():
  product_list = endpoints.get_products()

  # The length is a hard code result from the sandbox.  Merely to test the
  # iteration over the product api endpoint
  assert isinstance(product_list, list)
  # assert(len(product_list), 424)