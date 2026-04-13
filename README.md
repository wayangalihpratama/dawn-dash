# Dawn Dash (Hybrid-Automation Edition)

A "Semi-Auto" trading assistant for the Indonesia Stock Exchange (IDX) focusing on the **BSJP (Beli Sore Jual Pagi)** strategy.

## 🚀 Key Features

- **BSJP Signal Engine**: Curated signals based on Volume (1.5x Avg) and Price Change (>2%).
- **WIB Market Scheduler**: Aligned with Indonesia Market Hours (15:50 WIB Signal).
- **One-Click Execution**: Inline Telegram buttons with Stockbit Universal Links.
- **Dockerized Workflow**: Portable and easy to deploy.

## 📦 Startup & Commands

### 1. Configure Environment
```bash
cp .env.example .env
```
Edit `.env` and provide your `TELEGRAM_BOT_TOKEN`, `CHAT_ID`, and `METALPRICE_API_KEY`.

### 2. Run with Docker
All commands use the `./dc.sh` wrapper:
- **Startup**: `./dc.sh up -d`
- **Logs**: `./dc.sh logs -f`
- **Rebuild**: `./dc.sh up -d --build`
- **Testing**: `./dc.sh run --rm bot python -m pytest tests/`

### Phase 1: Infrastructure
- [x] Implement `GoldAPI` utility for MetalpriceAPI.
- [x] Setup persistence storage for historical prices.

### Phase 2: Logic & Notification
- [x] Implement "Dip Detection" algorithm.
- [x] Add HTML-formatted Telegram messages for gold updates.

## 🛠️ Architecture
- **Engine**: BSJP Scanner logic (`src/engine`).
- **Scheduler**: WIB-aware market clock (`src/scheduler`).
- **Notifier**: Telegram integration with HTML formatting (`src/notifier`).

## ⚖️ License
MIT
