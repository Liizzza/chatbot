import json
import urllib.request
import urllib


from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode


API_KEY = 'gbTLNjT_DtIGYldTPiy8mblU4Kv6Rk_ZKSsPjAg0_Cxr_7MgR2HJgdzoBbVEjjzSHDV5EN9JacV4UgRbZosTgbshm6mdIplQdpa6Iy5-CYBJC5wvpkMjYLuxVaa0ZXYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
DELIVERY_PATH = '/v3transactions/delivery/search'

HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Accept': 'application/json'}


def build_search_query_basic(location: str, type_of_food: str, category: str = None,
                             price: int = None, sort_by: str = None,
                             limit: int = 2) -> dict:
    query = {
        'term': type_of_food,
        'location': location,
    }

    if category is not None:
        query['category'] = category
    if price is not None:
        query['price'] = price
    if sort_by is not None:
        query['sort_by'] = sort_by
    if limit is not None:
        query['limit'] = limit

    return query


def build_search_query_delivery(location: str, type_of_food: str, /, category: str = None,
                                price: int = None) -> dict:
    query = {
        'term': type_of_food,
        'location': location
    }

    if category is not None:
        query['category'] = category
    if price is not None:
        query['price'] = price

    return query


def build_reviews_query(business_id: str, limit: int = 2, sort_by: str = 'yelp sort') -> dict:
    """Build a query for fetching Yelp reviews for a given business."""
    query = {
        'business_id': business_id,
        'limit': limit,
        'sort_by': sort_by
    }
    return query


def build_search_url(search_query: dict, parameter: str = BUSINESS_PATH,
                     reviews: bool = False) -> str:
    """creates a search url given the wanted parameters i.e term,location,catagory,price"""
    base_url = f'{API_HOST}{parameter}'
    if parameter == BUSINESS_PATH and reviews is True:
        url = f"{base_url}?"
    else:
        url = f"{base_url}?{urllib.parse.urlencode(search_query)}"
    return url


def build_reviews_url(business_id: str, limit: int = 2, sort_by: str = 'yelp_sort') -> str:
    """Create a URL for fetching Yelp reviews based on the provided parameters."""
    base_url = f'{API_HOST}{BUSINESS_PATH}{business_id}/reviews'
    url_params = {
        'limit': limit,
        'sort_by': sort_by
    }
    url = f"{base_url}?{urllib.parse.urlencode(url_params)}"
    return url


def request(url: str, headers):
    """
    sends a url request based off url and headers
    """

    try:
        req = urllib.request.Request(url, headers = headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data

    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example business_id
    business_id = 'vu6PlPyKptsT6oEq50qOzA'
    # Build the Yelp reviews query
    reviews_query = build_reviews_query(business_id, limit = 1, sort_by = 'yelp_sort')
    # Build the Yelp reviews URL
    reviews_url = build_reviews_url(**reviews_query)
    # Make Yelp API request
    response_data = request(reviews_url, HEADERS)
    # Process the response data as needed
    if response_data:
        print(json.dumps(response_data, indent = 2))
