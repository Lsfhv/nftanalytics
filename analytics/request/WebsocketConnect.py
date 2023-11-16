import json
from websockets import connect 
import os
class WsConnect:
    def __init__(self) -> None:
        self.isConnected = False
        self.ws = None
        self.subscriptionToQueue = {}

    async def connect(self) -> None:
        """Connect to ws endpoint
        """     
        self.ws = await connect(f"wss://mainnet.infura.io/ws/v3/{os.environ['INFURAAPIKEY']}")
        
        self.isConnected = True
    
    async def startHandlingMessages(self):
        """Start handling messages

        If subscription response, save the response
        If response to an event, send it to self.q for processing

        """
        while True:
            if self.ws == None or not self.isConnected:
                return 

            message = await self.ws.recv()
            message = json.loads(message)
            
            if 'id' in message and 'result' in message:
                self.subscriptionToQueue[message['result']] = self.subscriptionToQueue[message['id']]
            else:
                await self.subscriptionToQueue[message['params']['subscription']].put(message)

    async def sendMessage(self, message, queue):
        self.subscriptionToQueue[message['id']] = queue

        message = json.dumps(message)
        await self.ws.send(message)
            
    