import pytest
import requests
from unittest.mock import patch, MagicMock
from src.utils.pegadaian_api import PegadaianAPI


@pytest.fixture
def api():
    return PegadaianAPI()


def test_fetch_latest_price_success(api):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": {
            "hargaBeli": "27470",
            "hargaJual": "26090",
            "tglBerlaku": "2026-04-23",
            "isHargaBeliUp": True,
            "isHargaJualUp": True,
        },
    }

    with patch("requests.get", return_value=mock_response):
        result = api.fetch_latest_price()

        assert result["price_idr_gram"] == 2747000.0
        assert result["sell_price_idr_gram"] == 2609000.0
        assert result["currency"] == "IDR"
        assert result["provider"] == "Pegadaian (Direct)"
        assert result["date"] == "2026-04-23"


def test_fetch_latest_price_list_format(api):
    """Handle case where 'data' is a list instead of a dict."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": [
            {
                "hargaBeli": "27470",
                "hargaJual": "26090",
                "tglBerlaku": "2026-04-23",
            }
        ],
    }

    with patch("requests.get", return_value=mock_response):
        result = api.fetch_latest_price()
        assert result["price_idr_gram"] == 2747000.0


def test_fetch_latest_price_missing_field(api):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": "success",
        "data": {"invalid": "data"},
    }

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(Exception, match="Missing 'hargaBeli'"):
            api.fetch_latest_price()


def test_fetch_latest_price_network_error(api):
    with patch(
        "requests.get", side_effect=requests.RequestException("Timeout")
    ):
        with pytest.raises(Exception, match="Failed to fetch gold price"):
            api.fetch_latest_price()
