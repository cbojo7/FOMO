import requests

r = requests.get(
    'http://localhost:8000/catalog/api',
    auth=('chelsey.stockton@gmail.com', '0000000a'),
    params=dict(
        category='instruments',
        product=None,
        max_price=None,
        page=None
        )
    )
print(r.json())