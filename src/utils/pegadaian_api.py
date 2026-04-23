import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class PegadaianAPI:
    """
    Direct wrapper for Pegadaian's internal API to fetch real-time gold prices.
    """

    URL = "https://sahabat.pegadaian.co.id/gold/prices/savings"
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Referer": "https://www.pegadaian.co.id/",
    }

    def fetch_latest_price(self):
        """
        Fetches the latest Pegadaian Tabungan Emas price.
        Returns the 'buy' price per gram (harga jual Pegadaian).
        """
        try:
            # We use a session or simple request. Pegadaian API is public but expects a browser UA.
            response = requests.get(self.URL, headers=self.HEADERS, timeout=10)
            response.raise_for_status()
            data = response.json()

            # The API response structure observed:
            # {
            #   "data": [
            #     {
            #       "buy": 1238000,
            #       "sell": 1149000,
            #       "date": "2026-04-23 09:00:00",
            #       ...
            #     }
            #   ],
            #   "status": "success"
            # }
            price_data = data.get("data", [])
            logger.info(
                f"Price data type: {type(price_data)}, content: {price_data}"
            )
            if not price_data:
                raise Exception("Empty data received from Pegadaian API.")

            if isinstance(price_data, list):
                latest = price_data[0]
            else:
                latest = price_data
            # Pegadaian Tabungan Emas API returns prices for 0.01 gram.
            # hargaBeli: Price at which customers BUY (Rp 27,470 -> Rp 2,747,000/gram)
            # hargaJual: Price at which customers SELL (Rp 26,090 -> 2.6M/gram)

            # Map keys based on observed response:
            # {'hargaBeli': '27470', 'hargaJual': '26090', ...}
            raw_buy = float(latest.get("hargaBeli", 0))
            raw_sell = float(latest.get("hargaJual", 0))

            if not raw_buy:
                raise Exception(
                    "Missing 'hargaBeli' price in Pegadaian response."
                )

            # Convert 0.01g to 1g
            buy_price_gram = raw_buy * 100
            sell_price_gram = raw_sell * 100

            return {
                "price_idr_gram": buy_price_gram,
                "sell_price_idr_gram": sell_price_gram,
                "currency": "IDR",
                "timestamp": datetime.now().isoformat(),
                "provider": "Pegadaian (Direct)",
                "date": latest.get("tglBerlaku"),
                "unit": "1 gram",
                "raw_001g": {"buy": raw_buy, "sell": raw_sell},
            }

        except Exception as e:
            logger.error(
                f"Error fetching gold price from Pegadaian: {e}",
                exc_info=True,
            )
            raise Exception(f"Failed to fetch gold price: {e}")
