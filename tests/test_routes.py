import pytest
from unittest.mock import patch


def test_get_empty_inventory(client):
    resp = client.get('/inventory')
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_crud_lifecycle(client):
    # Create
    data = {'name': 'Widget', 'quantity': 10}
    resp = client.post('/inventory', json=data)
    assert resp.status_code == 201
    item = resp.get_json()
    item_id = item['id']

    # Read
    resp = client.get(f'/inventory/{item_id}')
    assert resp.status_code == 200
    assert resp.get_json()['name'] == 'Widget'

    # Update
    resp = client.patch(f'/inventory/{item_id}', json={'quantity': 5})
    assert resp.status_code == 200
    assert resp.get_json()['quantity'] == 5

    # Delete
    resp = client.delete(f'/inventory/{item_id}')
    assert resp.status_code == 204

    # Confirm gone
    resp = client.get(f'/inventory/{item_id}')
    assert resp.status_code == 404


@patch('app.external_api.requests.get')
def test_fetch_external_api(mock_get, client):
    # Mock barcode lookup
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = {
        'status': 1, 'product': {'product_name': 'TestProduct'}}
    resp = client.get('/inventory/fetch?barcode=12345')
    assert resp.status_code == 200
    assert resp.get_json()['product_name'] == 'TestProduct'

    # Missing query
    resp = client.get('/inventory/fetch')
    assert resp.status_code == 400