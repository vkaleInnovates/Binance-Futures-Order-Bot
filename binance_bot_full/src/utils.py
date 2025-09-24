import logging, os, time, json, re
from dotenv import load_dotenv

load_dotenv()

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bot.log")

def setup_logger():
    logger = logging.getLogger("binance_bot")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

logger = setup_logger()

def validate_symbol(sym):
    # basic validation: uppercase letters + digits, e.g., BTCUSDT
    if not isinstance(sym, str):
        return False, "Symbol must be a string"
    if not re.fullmatch(r'[A-Z0-9]{4,12}', sym):
        return False, "Symbol should be 4-12 chars alphanumeric uppercase (e.g., BTCUSDT)"
    return True, None

def validate_side(side):
    if side.upper() not in ('BUY', 'SELL'):
        return False, "Side must be BUY or SELL"
    return True, None

def validate_quantity(q):
    try:
        qf = float(q)
        if qf <= 0:
            return False, "Quantity must be > 0"
        return True, None
    except Exception as e:
        return False, "Quantity must be a number"

def validate_price(p):
    try:
        pf = float(p)
        if pf <= 0:
            return False, "Price must be > 0"
        return True, None
    except Exception as e:
        return False, "Price must be a number"

# Binance client wrapper (mock by default)
class BinanceClientWrapper:
    def __init__(self, mode='mock'):
        self.mode = mode
        # lazy import to avoid failing when python-binance isn't installed
        self.client = None
        if self.mode == 'live':
            try:
                from binance.client import Client
                import os
                api_key = os.getenv('BINANCE_API_KEY')
                api_secret = os.getenv('BINANCE_API_SECRET')
                if not api_key or not api_secret:
                    raise EnvironmentError('API key/secret not set in .env')
                self.client = Client(api_key, api_secret)
            except Exception as e:
                logger.error(f"Failed to initialize live client: {e}")
                raise

    def place_market_order(self, symbol, side, quantity):
        logger.info(f"Placing market order | mode={self.mode} | {symbol} {side} {quantity}")
        if self.mode == 'mock':
            # Simulate an order response
            resp = {
                'orderId': int(time.time()),
                'symbol': symbol,
                'status': 'FILLED',
                'side': side,
                'executedQty': str(quantity),
                'price': 'market'
            }
            logger.debug(json.dumps(resp))
            return resp
        else:
            # Live mode – use binance client (USDT-M Futures)
            try:
                resp = self.client.futures_create_order(symbol=symbol, side=side, type='MARKET', quantity=quantity)
                logger.debug(str(resp))
                return resp
            except Exception as e:
                logger.error(f"Live market order failed: {e}")
                raise

    def place_limit_order(self, symbol, side, quantity, price, time_in_force='GTC'):
        logger.info(f"Placing limit order | mode={self.mode} | {symbol} {side} {quantity} @ {price}")
        if self.mode == 'mock':
            resp = {
                'orderId': int(time.time()),
                'symbol': symbol,
                'status': 'NEW',
                'side': side,
                'origQty': str(quantity),
                'price': str(price)
            }
            logger.debug(json.dumps(resp))
            return resp
        else:
            try:
                resp = self.client.futures_create_order(symbol=symbol, side=side, type='LIMIT', quantity=quantity, price=str(price), timeInForce=time_in_force)
                logger.debug(str(resp))
                return resp
            except Exception as e:
                logger.error(f"Live limit order failed: {e}")
                raise
