import requests

BASE_URL = 'https://world.openfoodfacts.org'


def fetch_product_by_barcode(barcode: str):
    url = f'{BASE_URL}/api/v0/product/{barcode}.json'
    resp = requests.get(url, timeout=5)
    if resp.ok and resp.json().get('status') == 1:
        return resp.json()['product']
    return None


def fetch_product_by_name(name: str):
    url = f'{BASE_URL}/cgi/search.pl'
    params = {'search_terms': name,
              'search_simple': 1, 'json': 1, 'page_size': 1}
    resp = requests.get(url, params=params, timeout=5)
    data = resp.json()
    if data.get('products'):
        return data['products'][0]
    return None