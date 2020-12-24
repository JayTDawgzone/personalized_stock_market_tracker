# import requests
from config import api_key, sandbox_key
import json
from datetime import datetime
import pytz

import websocket

def on_message(ws, message):
    result = json.loads(message)
    try:
        timestamp = int(result['data'][0]['t'])
        timestamp /= 1000
        utc = pytz.utc.localize(datetime.utcfromtimestamp(timestamp))
        pst = utc.astimezone(pytz.timezone("America/Los_Angeles")).strftime('%Y-%m-%d %H:%M:%S')

        symbol = result['data'][0]['s']
        volume = result['data'][0]['v']
        price = result['data'][0]['p']

        print(f'Ticker: {symbol}, Price: {price}, Volume: {volume}, Timestamp: {pst} ', flush=True)
    except:
        pass


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    # ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"TSLA"}')
    # ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    # ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={api_key}",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
