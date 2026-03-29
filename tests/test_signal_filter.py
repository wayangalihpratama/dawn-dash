import pytest
import json
from src.engine.signal_filter import SignalScanner


@pytest.fixture
def mock_scanner(tmp_path):
    # Create a temporary tickers file
    d = tmp_path / "utils"
    d.mkdir()
    p = d / "kompas100.json"
    p.write_text(json.dumps({"tickers": ["BBCA", "BBRI", "BMRI"]}))
    return SignalScanner(tickers_path=str(p))


def test_filter_index_inclusion(mock_scanner):
    data = [
        {
            "symbol": "BBCA",
            "price_change_pct": 2.5,
            "volume": 1000,
            "avg_volume_20": 500,
        },  # Valid
        {
            "symbol": "ABCD",
            "price_change_pct": 3.0,
            "volume": 1000,
            "avg_volume_20": 500,
        },  # Not in index
    ]
    results = mock_scanner.filter_bsjp(data)
    assert len(results) == 1
    assert results[0]["symbol"] == "BBCA"


def test_filter_price_threshold(mock_scanner):
    data = [
        {
            "symbol": "BBCA",
            "price_change_pct": 2.1,
            "volume": 1000,
            "avg_volume_20": 500,
        },  # Valid (>2%)
        {
            "symbol": "BBRI",
            "price_change_pct": 1.9,
            "volume": 1000,
            "avg_volume_20": 500,
        },  # Invalid (<=2%)
    ]
    results = mock_scanner.filter_bsjp(data)
    assert len(results) == 1
    assert results[0]["symbol"] == "BBCA"


def test_filter_volume_ratio(mock_scanner):
    data = [
        {
            "symbol": "BBCA",
            "price_change_pct": 2.5,
            "volume": 160,
            "avg_volume_20": 100,
        },  # Valid (1.6x)
        {
            "symbol": "BBRI",
            "price_change_pct": 2.5,
            "volume": 140,
            "avg_volume_20": 100,
        },  # Invalid (1.4x)
    ]
    results = mock_scanner.filter_bsjp(data)
    assert len(results) == 1
    assert results[0]["symbol"] == "BBCA"
    assert results[0]["volume_ratio"] == 1.6


def test_filter_empty_list(mock_scanner):
    assert mock_scanner.filter_bsjp([]) == []
