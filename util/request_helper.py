import requests
from util.log_helper import get_logger

AUCTIONAPI = "https://api.hypixel.net/skyblock/auctions"

LOGGER = get_logger(__name__)


def request_api(page_number: int = 0):
    result = requests.get(url=AUCTIONAPI, params={"page": page_number})
    json_data = result.json()

    if result.status_code != 200:
        LOGGER.warning("Unexpected status code: " + str(result.status_code))
        return {}
    
    if not json_data["success"]:
        raise ValueError("API request failed.")
    
    return json_data


def get_auction_page_json(page_number: int):
    json_data = request_api(page_number)

    return json_data


def get_total_page_count():
    json_data = request_api()

    return json_data["totalPages"]


def filter_page_by_properties(page: dict, properties: dict):
    results = []

    for item in page:
        for property, value in properties.items():
            if not item[property] or item[property] != value:
                break

            results.append(item)
            break
    
    return results


def get_auctions_by_item(item_name: str, bin: bool = False):
    total_pages = get_total_page_count()

    result = []

    for page_number in range(0, total_pages - 1):
        json_data = request_api(page_number)
        filtered_list = filter_page_by_properties(json_data["auctions"], {"item_name": item_name, "bin": bin})

        result = result + filtered_list

    return result