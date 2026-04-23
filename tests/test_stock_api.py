import pytest
import requests_mock
from src.utils.stock_api import StockAPI


@pytest.fixture
def stock_api():
    return StockAPI(api_key="test_key")


def test_fetch_market_data_success(stock_api):
    mock_response = {
        "status": "success",
        "data": {
            "results": [
                {
                    "symbol": "BBCA",
                    "change_percent": 2.5,
                    "volume": 1000000,
                    "volume_average": 500000,
                }
            ]
        },
    }

    with requests_mock.Mocker() as m:
        m.get("https://api.goapi.io/stock/idx/trending", json=mock_response)
        data = stock_api.fetch_market_data()

    assert len(data) == 1
    assert data[0]["symbol"] == "BBCA"
    assert data[0]["price_change_pct"] == 2.5
    assert data[0]["volume"] == 1000000
    assert data[0]["avg_volume_20"] == 500000


def test_fetch_market_data_empty_key():
    api = StockAPI(api_key=None)
    assert api.fetch_market_data() == []


def test_fetch_market_data_error_status(stock_api):
    mock_response = {"status": "error", "message": "Invalid Key"}

    with requests_mock.Mocker() as m:
        m.get("https://api.goapi.io/stock/idx/trending", json=mock_response)
        data = stock_api.fetch_market_data()

    assert data == []
