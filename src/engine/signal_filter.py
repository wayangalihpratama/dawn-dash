import json
import os
import logging

logger = logging.getLogger(__name__)


class SignalScanner:
    def __init__(self, tickers_path=None):
        if tickers_path is None:
            # Default to the internal path
            base_dir = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
            tickers_path = os.path.join(base_dir, "utils", "kompas100.json")

        self.kompas100 = self._load_tickers(tickers_path)

    def _load_tickers(self, path):
        """Load the list of valid tickers from a JSON file."""
        try:
            with open(path, "r") as f:
                data = json.load(f)
                return set(data.get("tickers", []))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load KOMPAS100 list: {e}")
            return set()

    def filter_bsjp(self, stock_data_list):
        """
        Filters a list of stock data objects based on BSJP criteria:
        - Price Change > 2%
        - Volume > 1.5x 20-day Average
        - Member of KOMPAS100

        :param stock_data_list: List of dicts with keys:
               'symbol', 'price_change_pct', 'volume', 'avg_volume_20'
        :return: List of valid signal candidates.
        """
        candidates = []
        for stock in stock_data_list:
            symbol = stock.get("symbol")
            price_change = stock.get("price_change_pct", 0)
            volume = stock.get("volume", 0)
            avg_volume = stock.get("avg_volume_20", 0)

            # 1. Index Check
            if symbol not in self.kompas100:
                continue

            # 2. Price Change Check (> 2%)
            if price_change <= 2.0:
                continue

            # 3. Volume Ratio Check (> 1.5x)
            if avg_volume > 0:
                vol_ratio = volume / avg_volume
                if vol_ratio > 1.5:
                    stock["volume_ratio"] = round(vol_ratio, 2)
                    candidates.append(stock)

        return candidates
