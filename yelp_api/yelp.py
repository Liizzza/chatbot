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

HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Accept': 'application/json'}




def build_search_url(search_query):
    base_url = f'{API_HOST}{SEARCH_PATH}'
    headers = {'Authorization': f'Bearer {API_KEY}', 'Accept': 'application/json'}

    # Combine headers and query parameters in the URL
    url = f"{base_url}?{urllib.parse.urlencode(search_query)}"

    return url


def request(url: str, headers):
    """
    sends a url request based off url and headers
    """

    try:
        # Make the API request using urllib.requests
        req = urllib.request.Request(url, headers = headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data

    except urllib.error.HTTPError as e:
        # Handle HTTP errors
        print(f"HTTP Error {e.code}: {e.reason}")
        return None

    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example search query
    search_query = {'term': 'pizza', 'location': 'New York'}
    # Build the Yelp search URL
    search_url = build_search_url(search_query)
    # Make Yelp API request
    response_data = request(search_url, HEADERS)
    # Process the response data as needed
    if response_data:
        print(json.dumps(response_data, indent = 2))
