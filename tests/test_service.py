import pytest
import tap_treez.service as service

@pytest.mark.vcr()
def test_get_token():
  token = service.get_token()

  assert isinstance(token, str)