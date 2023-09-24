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
@app.route('/slug/<address>')
def getslug(address):

    """
    Given an address, returns the name of the collection.
    """

    connection = PostgresConnection()
    
    response = connection.readonly(f"select * from slug where address='{escape(address).lower()}'")
    print(escape(address).lower())
    if len(response) == 0:
        return 'Not found'
    data = {"slug": response[0][-1]}
    
    data = json.dumps(data)
    print(data)
    return data

@sock.route('/volume')
def volume(ws):
    data = ws.receive()
    data = json.loads(data)

    data['address'] = data['address'].lower()
    
    asyncio.run(getVolumeMain(data['address'], data['params'], ws))

app.run()