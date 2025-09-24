# Binance Futures Order Bot - Starter Implementation

This repository contains a **starter, fully-implemented** assignment for the Binance USDT-M Futures Order Bot. It defaults to **safe mock mode** (simulates orders and logs them). You can enable live mode by providing Binance API keys in a `.env` file (see below).

## Structure
```
[project_root]/
├── src/
│   ├── market_orders.py
│   ├── limit_orders.py
│   ├── utils.py
│   └── advanced/
│       ├── oco.py
│       └── twap.py
├── bot.log
├── README.md
├── requirements.txt
└── report.pdf
```

## Setup (mock mode - recommended for development)
1. (Optional) Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Run any script in **mock** mode (default) — no real trades will be executed, only simulated and logged:
   ```bash
   python src/market_orders.py --symbol BTCUSDT --side BUY --quantity 0.001
   python src/limit_orders.py --symbol BTCUSDT --side SELL --quantity 0.001 --price 60000
   ```

## Enabling Live Mode (only if you know what you're doing)
1. Create a `.env` file in the project root with:
   ```env
   BINANCE_API_KEY=your_api_key_here
   BINANCE_API_SECRET=your_api_secret_here
   ```
2. Run with `--mode live`:
   ```bash
   python src/market_orders.py --symbol BTCUSDT --side BUY --quantity 0.001 --mode live
   ```
**WARNING:** Live mode will place real orders on Binance USDT-M Futures. Use testnet keys or be extremely careful.

## Files of interest
- `src/utils.py` — logging setup, input validation, and a `BinanceClientWrapper` abstraction. In mock mode it simulates responses.
- `src/market_orders.py` — CLI to place market orders.
- `src/limit_orders.py` — CLI to place limit orders.
- `src/advanced/oco.py` — Example OCO logic (simulated in mock mode).
- `src/advanced/twap.py` — Example TWAP execution (simulated by splitting orders into chunks).

## Logging
All actions are logged to `bot.log` in structured format (timestamp, level, message).

## Deliverables
- Implemented market & limit orders, validation & logging.
- Example advanced strategies (OCO, TWAP) implemented for evaluation (simulated).
- `report.pdf` containing a short summary (placeholder).

---
