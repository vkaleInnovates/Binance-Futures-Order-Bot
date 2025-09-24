#!/usr/bin/env python3
import argparse
from utils import validate_symbol, validate_side, validate_quantity, logger, BinanceClientWrapper

def main():
    parser = argparse.ArgumentParser(description='Place a market order (mock by default)')
    parser.add_argument('--symbol', required=True, help='Trading symbol e.g., BTCUSDT')
    parser.add_argument('--side', required=True, help='BUY or SELL')
    parser.add_argument('--quantity', required=True, help='Order quantity (e.g., 0.001)')
    parser.add_argument('--mode', choices=['mock','live'], default='mock', help='Run mode: mock or live (live requires .env API keys)')
    args = parser.parse_args()

    ok, err = validate_symbol(args.symbol)
    if not ok:
        logger.error(err)
        raise SystemExit(err)
    ok, err = validate_side(args.side)
    if not ok:
        logger.error(err)
        raise SystemExit(err)
    ok, err = validate_quantity(args.quantity)
    if not ok:
        logger.error(err)
        raise SystemExit(err)

    client = BinanceClientWrapper(mode=args.mode)
    resp = client.place_market_order(args.symbol, args.side.upper(), float(args.quantity))
    print('Order response:', resp)
    logger.info('Market order completed.')

if __name__ == '__main__':
    main()
