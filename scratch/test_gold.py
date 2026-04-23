import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.pegadaian_api import PegadaianAPI
import logging
import json

logging.basicConfig(level=logging.INFO)


def test_gold():
    print("--- Fetching Gold Price from Pegadaian ---")
    api = PegadaianAPI()
    try:
        data = api.fetch_latest_price()
        print(json.dumps(data, indent=2))
        print("\n✅ Success!")
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"\n❌ Failed: {e}")


if __name__ == "__main__":
    test_gold()
