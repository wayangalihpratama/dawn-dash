import requests
import logging

logger = logging.getLogger(__name__)


class GoldAPI:
    """
    Wrapper for Goapi.io to fetch local gold prices (Pegadaian).
    """

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.goapi.io/gold/pegadaian"

    def fetch_latest_price(self):
        """
        Fetches the latest Pegadaian gold price from Goapi.io.
        Returns the price per gram in IDR.
        """
        if not self.api_key:
            # Fallback for development/testing if key is missing
            logger.warning("GOAPI_KEY is not set. Using placeholder data.")
            return {
                "price_idr_gram": 1250000.0,
                "currency": "IDR",
                "timestamp": None,
                "date": "2026-04-13",
            }

        url = self.base_url
        headers = {"X-API-KEY": self.api_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()

            if result.get("status") != "success":
                error_msg = result.get("message", "Unknown Goapi error")
                raise Exception(f"Goapi Error: {error_msg}")

            # Goapi Pegadaian usually returns a list of prices.
            # We look for "Tabungan Emas" or the first available "Antam" price.
            data_list = result.get("data", [])
            if not data_list:
                raise Exception("No data received from Goapi Pegadaian.")

            # Priority: 1. Tabungan Emas, 2. First Item
            target = next(
                (
                    item
                    for item in data_list
                    if "Tabungan" in item.get("name", "")
                ),
                data_list[0],
            )

            # Price is usually in "buy" or "price" field
            price = target.get("price") or target.get("buy")
            if not price:
                raise Exception(
                    f"Price field not found in item: {target.get('name')}"
                )

            return {
                "price_idr_gram": float(price),
                "currency": "IDR",
                "timestamp": None,
                "date": target.get("date"),
            }

        except requests.RequestException as e:
            logger.error(f"Network error fetching gold price from Goapi: {e}")
            raise Exception(f"Failed to fetch gold price: {e}")
