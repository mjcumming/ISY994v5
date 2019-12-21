#!/usr/local/bin/python

import asyncio
import aiohttp
from websocket_event import Websocket_Event
import xml.etree.ElementTree as ET
import logging
logger = logging.getLogger(__name__)

headers = {
    "Sec-WebSocket-Protocol": "ISYSUB",
    "Origin" : "com.universal-devices.websockets.isy",
}


URL = "ws://"+'192.168.1.51'+"/rest/subscribe"


class Websocket_Client(object):

    def __init__(self,controller,address,port,username,password,https):
        self._address = address
        self._port = port
        self.controller = controller
        self._https = https
        self.auth = aiohttp.BasicAuth('admin','admin')
        self._connected = False
    
    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self,connected):
        self._connected = connected
        if self.controller:
            self.controller.websocket_connected(connected)

    async def connect(self):
        URL = "ws://"+self._address+"/rest/subscribe"
        session = aiohttp.ClientSession()
        async with session.ws_connect(URL,headers=headers,auth=self.auth) as ws:

            async for msg in ws:
                #print('Message received from server:', msg)
                #logger.debug('Websocket Message: {}'.format(message))
                if msg.type == aiohttp.WSMsgType.TEXT:
                    try:
                        event_node = ET.fromstring (msg.data)        
                        
                        if event_node.tag == 'Event':
                            event = Websocket_Event(event_node)

                            if event.valid:
                                print (event)
                                if self.controller:
                                    self.controller.websocket_event(event)
                    
                    except Exception as ex:
                        logger.error('Websocket On Message Error {}'.format(ex))
'''
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                    else:
                        await ws.send_str(msg.data + '/answer')
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
'''


if __name__ == '__main__':
    try:
        wsc = Websocket_Client(False,"192.168.1.51",80,'admin','admin',False)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(wsc.connect())

    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")
