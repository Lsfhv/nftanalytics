from request.WebsocketConnect import WsConnect
import json

class Marketplace:
    def __init__(self, topic, ws):
        self.topic = topic
        self.ws = ws
        
    async def start(self):
        data = {"id": self.topic, "method":"eth_subscribe"}
        params = {"topics": [self.topic]}
        data["params"] = ["logs", params]
        data = json.dumps(data)

        await self.ws.ws.send(data)


    
    
    
