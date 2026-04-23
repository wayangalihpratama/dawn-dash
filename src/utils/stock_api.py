import requests
import logging

logger = logging.getLogger(__name__)


class StockAPI:
    """
    Wrapper for Goapi.io to fetch real-time IDX stock data.
    """

    def __init__(self, api_key=None):
        self.api_key = api_key
        # Goapi IDX market movers endpoint (no /v1)
        self.base_url = "https://api.goapi.io/stock/idx"

    def fetch_market_data(self):
        """
        Fetches market data for filtering (BSJP logic).
        Returns a list of dictionaries following the SignalScanner format.
        """
        if not self.api_key:
            logger.warning("GOAPI_KEY is not set. Returning empty data.")
            return []

        # Trending stocks endpoint
        url = f"{self.base_url}/trending"
        headers = {"X-API-KEY": self.api_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()

            if result.get("status") != "success":
                logger.error(f"Goapi Error: {result.get('message')}")
                return []

            raw_stocks = result.get("data", {}).get("results", [])

            # Map Goapi fields to Dawn Dash engine format
            mapped_data = []
            for item in raw_stocks:
                mapped_data.append(
                    {
                        "symbol": item.get("symbol"),
                        "price_change_pct": float(
                            item.get("change_percent", 0)
                        ),
                        "volume": int(item.get("volume", 0)),
                        # Goapi might not provide 20D Avg in one call;
                        # for real logic, we might need a separate endpoint or
                        # assume a baseline if missing.
                        "avg_volume_20": int(
                            item.get("volume_average", 1000000)
                        ),
                    }
                )

            return mapped_data

        except requests.RequestException as e:
            logger.error(f"Error fetching stock data: {e}")
            return []
