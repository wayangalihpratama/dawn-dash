# Dawn Dash (Hybrid-Automation Edition)

A "Semi-Auto" trading assistant for the Indonesia Stock Exchange (IDX) focusing on the BSJP (Beli Sore Jual Pagi) strategy.

## 🚀 Quick Start

### 1. Initial Setup
Configure your environment by copying the example file:
```bash
cp .env.example .env
```
Edit `.env` and provide your `TELEGRAM_BOT_TOKEN` and `CHAT_ID`.

### 2. Execution Commands
All commands use the standardized `./dc.sh` Docker wrapper:

- **Startup**: `./dc.sh up -d`
- **Rebuild**: `./dc.sh up -d --build`
- **Logs**: `./dc.sh logs -f`
- **Shutdown**: `./dc.sh down`
- **Run Tests**: `./dc.sh run --rm bot python -m pytest tests/`

---

## 🛠️ Project Structure
- `src/`: Core Python source code.
- `docs/`: Shared documentation (LLD, Feature Specs).
- `agent_docs/`: Internal sprint artifacts and user stories.
- `tests/`: Automated test suites.

## ⚖️ License
MIT
