import json
import urllib.request
import argparse
import pprint
import sys
import urllib


from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode


API_KEY = 'gbTLNjT_DtIGYldTPiy8mblU4Kv6Rk_ZKSsPjAg0_Cxr_7MgR2HJgdzoBbVEjjzSHDV5EN9JacV4UgRbZosTgbshm6mdIplQdpa6Iy5-CYBJC5wvpkMjYLuxVaa0ZXYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'


def build_search_url(search_query):
    base_url = f'{API_HOST}{SEARCH_PATH}'
    headers = {'Authorization': f'Bearer {API_KEY}', 'Accept': 'application/json'}

    url = f"{base_url}?/{headers}{urllib.parse.urlencode(search_query)}"

    return url
