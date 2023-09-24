from flask import Flask
from flask_sock import Sock
from api.GetVolume import getVolumeMain
import json
import asyncio

app = Flask(__name__)
sock = Sock(app)


@sock.route('/volume')
def volume(ws):
    data = ws.receive()
    data = json.loads(data)
    print("did any data come", data)
    
    asyncio.run(getVolumeMain(data['address'], data['params'], ws))

app.run()