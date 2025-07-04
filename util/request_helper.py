import requests
from util.log_helper import get_logger

AUCTIONAPI = "https://api.hypixel.net/skyblock/auctions"

LOGGER = get_logger(__name__)


def get_auction_page_json(page_number):
    result = requests.get(url=AUCTIONAPI, params={"page": page_number})
    json_data = result.json()

    if not result.status_code != 200:
        LOGGER.warning("Unexpected status code: " + result.status_code)
        return {}
    
    if not json_data["success"]:
        raise ValueError("API request failed.")

    print(json_data)
    return json_data


def get_total_page_count():
    result = requests.get(url=AUCTIONAPI)
    json_data = result.json()

    if not result.status_code != 200:
        LOGGER.warning("Unexpected status code: " + result.status_code)
        return {}
    
    if not json_data["success"]:
        raise ValueError("API request failed.")
    
    return json_data["totalPages"]

get_auction_page_json(5)