import json
import urllib.request
import urllib

from urllib.error import HTTPError
from urllib.parse import quote


API_KEY = 'gbTLNjT_DtIGYldTPiy8mblU4Kv6Rk_ZKSsPjAg0_Cxr_7MgR2HJgdzoBbVEjjzSHDV5EN9JacV4UgRbZosTgbshm6mdIplQdpa6Iy5-CYBJC5wvpkMjYLuxVaa0ZXYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'
DELIVERY_PATH = '/v3/transactions/delivery/search'
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Accept': 'application/json'}


def build_search_query_basic(location: str, type_of_food: str, category: str = None,
                             price: int = None, sort_by: str = None,
                             limit: int = 2) -> dict:
    query = {
        'location': location,
        'term': type_of_food,
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
        'location': location,
        'term': type_of_food
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


def build_search_url(search_query: dict, parameter: str = SEARCH_PATH,
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


def format_reviews_data(reviews_data: dict) -> str:
    """
    Format Yelp reviews data into a string for easy reading.
    """
    total_reviews = reviews_data.get('total', 0)
    formatted_reviews = [f"Total: {total_reviews} reviews"]

    for review in reviews_data.get('reviews', []):
        user_name = review['user'].get('name', 'Unknown User')
        rating = review.get('rating', 'N/A')
        text = review.get('text', 'No review text available')

        formatted_review = f"\nUser: {user_name}\nRating: {rating}\nReview: {text}"
        formatted_reviews.append(formatted_review)

    return ''.join(formatted_reviews)


def format_business_data(business_data: dict) -> str:
    ''''
    Format Yelp business data into a string for easy reading.
    '''

    formatted_businesses = []

    for business in business_data.get('businesses'):
        name = business.get('name', 'Unknown business')
        image = business.get('image_url', 'No image available')
        website = business.get('url', 'No website available')
        rating = business.get('rating', 'N/A')
        review_count = business.get('review_count', 0)
        categories = ', '.join(category['title'] for category in business.get('categories', []))
        price = business.get('price', 'N/A')
        address = ', '.join(business.get('location', {}).get('display_address', []))
        phone = business.get('display_phone', 'N/A')

        formatted_business = (
            f"\nName: {name}! {rating} stars, {review_count} reviews\nPrice: {price} | Categories: {categories}\n"
            f"Website: {website}\nImage URL: {image}\n"
            f"Located at {address} | Call {phone}\n"
        )
        formatted_businesses.append(formatted_business)

    return ''.join(formatted_businesses)


def format_delivery_data(delivery_data: dict) -> str:
    formatted_delivery_data = []

    total_deliveries = delivery_data.get('total', 0)
    formatted_delivery_data.append(f"Total Deliveries: {total_deliveries}")

    for delivery in delivery_data.get('businesses', []):
        name = delivery.get('name', 'Unknown Business')
        rating = delivery.get('rating', 'N/A')
        review_count = delivery.get('review_count', 0)
        image_url = delivery.get('image_url', 'No image available')
        url = delivery.get('url', 'No website available')
        categories = ', '.join(category['title'] for category in delivery.get('categories', []))

        formatted_delivery = (
            f"\nName: {name}! {rating} stars, {review_count} reviews\n"
            f"Categories: {categories}\n"
            f"Website: {url}\nImage URL: {image_url}\n"
        )

        formatted_delivery_data.append(formatted_delivery)

    return ''.join(formatted_delivery_data)


def grab_business_id(business_data: dict, desired_name: str) -> str:
    for business in business_data.get('businesses', []):
        if desired_name in business.get('name', ''):
            return business.get('id')

    return None


def find_and_print_restaurant_details(search_query: dict):
    business_search_query = build_search_query_basic(**search_query)
    business_search_url = build_search_url(business_search_query)

    business_search_response = request(business_search_url, HEADERS)

    if business_search_response:
        print(format_business_data(business_search_response))
    else:
        print("No data found! Error occured, please retry.")


def find_and_print_delivery_details(search_query: dict):
    delivery_query = build_search_query_basic(**search_query)
    delivery_url = build_search_url(delivery_query, DELIVERY_PATH)
    delivery_data = request(delivery_url, HEADERS)

    if delivery_data:
        print(format_delivery_data(delivery_data))
    else:
        print("Error occured, please retry.")


def find_and_print_rating_details(search_query: dict):
    reviews_query = build_reviews_query(**search_query)
    reviews_url = build_reviews_url(**reviews_query)

    response_data = request(reviews_url, HEADERS)

    if response_data:
        print(format_reviews_data(response_data))
    else:
        print('None! Sorry something went wrong')

if __name__ == "__main__":
    print('hi')
