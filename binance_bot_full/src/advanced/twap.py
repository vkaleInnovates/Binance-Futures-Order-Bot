#!/usr/bin/env python3
"""TWAP (simulated): split an order into n chunks and place sequential market orders (mock by default).

Usage:
python src/advanced/twap.py --symbol BTCUSDT --side BUY --quantity 0.01 --chunks 5 --interval 1 --mode mock
"""
import argparse, time
from utils import validate_symbol, validate_side, validate_quantity, logger, BinanceClientWrapper

def main():
    parser = argparse.ArgumentParser(description='Simulated TWAP execution (mock mode by default)')
    parser.add_argument('--symbol', required=True)
    parser.add_argument('--side', required=True)
    parser.add_argument('--quantity', required=True)
    parser.add_argument('--chunks', type=int, default=5, help='Number of parts to split')
    parser.add_argument('--interval', type=float, default=1.0, help='Seconds between chunks (short for simulation)')
    parser.add_argument('--mode', choices=['mock','live'], default='mock')
    args = parser.parse_args()

    for check_fn, val in [(validate_symbol, args.symbol), (validate_side, args.side), (validate_quantity, args.quantity)]:
        ok, err = check_fn(val)
        if not ok:
            logger.error(err)
            raise SystemExit(err)

    total_qty = float(args.quantity)
    per_chunk = total_qty / args.chunks
    client = BinanceClientWrapper(mode=args.mode)
    logger.info(f"Starting TWAP: {args.chunks} chunks, {per_chunk} each")
    results = []
    for i in range(args.chunks):
        logger.info(f"Placing chunk {i+1}/{args.chunks}")
        resp = client.place_market_order(args.symbol, args.side.upper(), per_chunk)
        results.append(resp)
        time.sleep(args.interval)
    print('TWAP results:', results)
    logger.info('TWAP simulation completed.')

if __name__ == '__main__':
    main()
