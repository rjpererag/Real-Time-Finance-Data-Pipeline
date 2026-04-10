from .ws.binance import BinanceWebsocket


class WebsocketWrapper:
    def __init__(self):
        self.binance = BinanceWebsocket
