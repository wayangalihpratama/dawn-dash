import unittest
import requests
from unittest.mock import patch, MagicMock
from src.utils.gold_api import GoldAPI


class TestGoldAPI(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_key"
        self.gold_api = GoldAPI(api_key=self.api_key)

    def test_troy_oz_to_gram_conversion(self):
        # 1 Troy Oz = 31.1035 Grams
        troy_oz_price = 2000.0  # USD per Troy Oz
        expected_gram_price = 2000.0 / 31.1035

        calculated_price = self.gold_api.convert_to_gram(troy_oz_price)
        self.assertAlmostEqual(calculated_price, expected_gram_price, places=4)

    @patch("src.utils.gold_api.requests.get")
    def test_fetch_latest_price_success(self, mock_get):
        # Mock response for MetalpriceAPI Latest
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "base": "USD",
            "rates": {
                "XAU": 0.00045,  # 1 USD = 0.00045 XAU -> 1 XAU = 2222.22 USD
                "IDR": 15000.0,  # 1 USD = 15000 IDR
            },
        }
        mock_get.return_value = mock_response

        data = self.gold_api.fetch_latest_price()

        # 1 XAU = 1 / 0.00045 = 2222.22 USD
        # 2222.22 USD * 15000 IDR = 33,333,333.33 IDR per Troy Oz
        # 33,333,333.33 / 31.1035 = 1,071,690.75 IDR per Gram

        self.assertIn("price_idr_gram", data)
        self.assertGreater(data["price_idr_gram"], 1000000)
        self.assertEqual(data["currency"], "IDR")

    @patch("src.utils.gold_api.requests.get")
    def test_fetch_latest_price_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("500 Server Error")
        )
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            self.gold_api.fetch_latest_price()


if __name__ == "__main__":
    unittest.main()
