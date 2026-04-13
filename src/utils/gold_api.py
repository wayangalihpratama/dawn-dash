import requests
import logging

logger = logging.getLogger(__name__)


class GoldAPI:
    TROY_OZ_TO_GRAM = 31.1035

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.metalpriceapi.com/v1"

    def convert_to_gram(self, troy_oz_price):
        """Converts price per troy ounce to price per gram."""
        return troy_oz_price / self.TROY_OZ_TO_GRAM

    def fetch_latest_price(self):
        """
        Fetches the latest gold price in USD and exchange rate for IDR,
        then calculates the price per gram in IDR.
        """
        if not self.api_key:
            raise ValueError("API Key for MetalpriceAPI is not set.")

        url = (
            f"{self.base_url}/latest?api_key={self.api_key}"
            "&base=USD&symbols=XAU,IDR"
        )

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                error_info = data.get("error", {}).get(
                    "info", "Unknown API error"
                )
                raise Exception(f"API Error: {error_info}")

            rates = data.get("rates", {})
            xau_rate = rates.get("XAU")  # 1 USD = x XAU
            idr_rate = rates.get("IDR")  # 1 USD = y IDR

            if not xau_rate or not idr_rate:
                raise Exception("Missing XAU or IDR rates in API response.")

            # 1 XAU = (1 / xau_rate) USD
            price_troy_oz_usd = 1 / xau_rate
            price_troy_oz_idr = price_troy_oz_usd * idr_rate
            price_gram_idr = self.convert_to_gram(price_troy_oz_idr)

            return {
                "price_idr_gram": round(price_gram_idr, 2),
                "currency": "IDR",
                "timestamp": data.get("timestamp"),
                "date": data.get("date"),
            }

        except requests.RequestException as e:
            logger.error(f"Network error fetching gold price: {e}")
            raise Exception(f"Failed to fetch gold price: {e}")
