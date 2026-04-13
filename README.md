# Dawn Dash (Hybrid-Automation Edition)

A "Semi-Auto" trading assistant for the Indonesia Stock Exchange (IDX) focusing on the **BSJP (Beli Sore Jual Pagi)** strategy.

## 🚀 Key Features

- **Real-Time Data**: Integrated with Goapi.io for live Stockbit/IDX and Pegadaian Gold prices.
- **BSJP Signal Engine**: Curated signals based on Volume (1.5x Avg) and Price Change (>2%).
- **WIB Market Scheduler**: Aligned with Indonesia Market Hours (15:50 WIB Signal).
- **One-Click Execution**: Inline Telegram buttons with Stockbit Universal Links.
- **Gold Dip Monitoring**: Automated alerts for Pegadaian "Buy the Dip" opportunities.

## 📦 Startup & Commands

### 1. Configure Environment
```bash
cp .env.example .env
```
Edit `.env` and provide your `TELEGRAM_BOT_TOKEN`, `CHAT_ID`, and `GOAPI_KEY`.

### 2. Run with Docker
All commands use the `./dc.sh` wrapper:
- **Startup**: `./dc.sh up -d`
- **Logs**: `./dc.sh logs -f`
- **Rebuild**: `./dc.sh up -d --build`
- **Testing**: `./dc.sh run --rm bot python -m pytest tests/`

### Phase 1: Infrastructure
- [x] Implement `GoldAPI` utility for Pegadaian (Goapi.io).
- [x] Implement `StockAPI` for real-time IDX signals.
- [x] Setup persistence storage for historical prices.

### Phase 2: Logic & Notification
- [x] Implement "Dip Detection" algorithm.
- [x] Integrate real market movers into Daily Journals.

## 🛠️ Architecture
- **Engine**: BSJP Scanner logic (`src/engine`).
- **Scheduler**: WIB-aware market clock (`src/scheduler`).
- **Notifier**: Telegram integration with HTML formatting (`src/notifier`).

## ⚖️ License
MIT
