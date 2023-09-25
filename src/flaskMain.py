from flask import Flask
from flask_sock import Sock
from api.GetVolume import getVolumeMain
import json
import asyncio
from markupsafe import escape
from Postgresql import PostgresConnection
from flask_cors import CORS

app = Flask(__name__)
sock = Sock(app)

CORS(app)

@app.route('/activity/<slug>')
def activity(slug):
    slug = escape(slug)

    address = PostgresConnection().readonly(f"select address from slug where blur='{slug}'")[0][0]

    response = PostgresConnection().readonly(f"select * from transfers where address='{address}' order by time_updated DESC")

    data = {"result": response}
    
    data = json.dumps(data)
    return data

@app.route('/slug/<slug>')
def getAddress(slug):
    response = PostgresConnection().readonly(f"select * from slug where blur='{escape(slug)}'")
    data = json.dumps({"address": response[0]})
    return data

@sock.route('/volume')
def volume(ws):
    data = ws.receive()
    data = json.loads(data)
    response = PostgresConnection().readonly(f"select address from slug where blur='{data['slug']}'")
    asyncio.run(getVolumeMain(response[0][0], data['params'], ws))

app.run()