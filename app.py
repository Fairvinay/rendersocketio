# 🔥 MUST BE FIRST LINE
import eventlet
eventlet.monkey_patch()

import os
import ssl
import json
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from fyers_apiv3.FyersWebsocket import data_ws

app = Flask(__name__)
# SocketIO handles the "Connection: Upgrade" for you automatically
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")


# --- Fyers Callbacks ---
def on_message(message):
    # DIRECTLY emit to the frontend. No manual queues.
    # This sends the tick to every connected browser instantly.
    socketio.emit("market_data", message)


def on_open(fyers_instance, tickers):
    data_type = "SymbolUpdate"
    if tickers is None:
    	tickers = [ "BSE:SENSEX-INDEX", "NSE:NIFTY50-INDEX","NSE:NIFTYBANK-INDEX"]
    fyers_instance.subscribe(symbols=tickers, data_type=data_type)


# --- Global Socket Holder ---
fyers_socket = None


@socketio.on("connect")
def handle_connect():
    print("Browser connected via WebSocket")


@socketio.on("start_feed")
def handle_start_feed(data):
    """
    Frontend sends: { "accessToken": "...", "tickers": ["NSE:SBIN-EQ"] }
    """
    global fyers_socket
    token = data.get("accessToken")
    tickers = data.get("tickers", [])

    if fyers_socket is None:
        fyers_socket = data_ws.FyersDataSocket(
            access_token=token,
            litemode=True,
            reconnect=True,
            on_connect=lambda: on_open(fyers_socket, tickers),
            on_message=on_message,
        )
        fyers_socket.connect()
        emit("status", {"msg": "Fyers Socket Connected"})


if __name__ == "__main__":
    #cert_file = os.path.join(os.path.dirname(__file__), "ssl.crt/server.crt")
    #key_file = os.path.join(os.path.dirname(__file__), "ssl.key/server.key")
    # Use socketio.run instead of app.run
    #context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # context.load_cert_chain(cert_file, key_file)
    #context.load_cert_chain("ssl.crt/server.crt", "ssl.key/server.key")
    # Use socketio.run instead of app.run
    socketio.run(app, host="0.0.0.0", port=3000, debug=False)
