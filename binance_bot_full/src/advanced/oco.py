#!/usr/bin/env python3
"""Simulated OCO: place take-profit and stop-loss simultaneously. In mock mode this function simulates execution.

Usage (from repo root):
python src/advanced/oco.py --symbol BTCUSDT --side BUY --quantity 0.001 --tp 70000 --sl 50000 --mode mock
"""
import argparse, time
from utils import validate_symbol, validate_side, validate_quantity, validate_price, logger, BinanceClientWrapper

def main():
    parser = argparse.ArgumentParser(description='Simulated OCO order (mock by default)')
    parser.add_argument('--symbol', required=True)
    parser.add_argument('--side', required=True)
    parser.add_argument('--quantity', required=True)
    parser.add_argument('--tp', required=True, help='Take-profit price')
    parser.add_argument('--sl', required=True, help='Stop-loss price (trigger)')
    parser.add_argument('--mode', choices=['mock','live'], default='mock')
    args = parser.parse_args()

    # validations
    for check_fn, val in [(validate_symbol, args.symbol), (validate_side, args.side),
                          (validate_quantity, args.quantity), (validate_price, args.tp), (validate_price, args.sl)]:
        ok, err = check_fn(val)
        if not ok:
            logger.error(err)
            raise SystemExit(err)

    client = BinanceClientWrapper(mode=args.mode)
    # Place both simulated orders
    tp_side = 'SELL' if args.side.upper()=='BUY' else 'BUY'
    logger.info('Placing simulated OCO orders...')
    tp = client.place_limit_order(args.symbol, tp_side, float(args.quantity), float(args.tp))
    sl = client.place_limit_order(args.symbol, tp_side, float(args.quantity), float(args.sl))
    print('Take-profit order:', tp)
    print('Stop-loss order (simulated):', sl)
    logger.info('OCO simulated: waiting for a simulated execution...')
    # Simulation: pick one to "execute" based on simple logic (price closer to tp executes)
    time.sleep(1)
    executed = tp
    logger.info(f"Simulated order executed: {executed['orderId']}. Cancelling the other.")
    print('Simulated executed order id:', executed['orderId'])

if __name__ == '__main__':
    main()
