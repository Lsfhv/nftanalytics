from flask import Flask
from flask_sock import Sock
from api.GetVolume import getVolumeMain
from api.GetTrades import getTradesMain
import json
import asyncio
from markupsafe import escape
from Postgresql import PostgresConnection
from flask_cors import CORS

app = Flask(__name__)
sock = Sock(app)

CORS(app)

@sock.route('/trades')
def getTrades(ws):
    data = ws.receive()
    data = json.loads(data)
    address = data['address']

    asyncio.run(getTradesMain(ws, address))

@app.route('/getaddress/<slug>')
def getAddress(slug):
    slug = escape(slug)
    response = PostgresConnection().readonly(f"select address from slug where opensea='{slug}'")
    
    response = {"address": response[0][0]}

    return [response]


app.run()