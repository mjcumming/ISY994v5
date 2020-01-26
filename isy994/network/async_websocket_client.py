#!/usr/local/bin/python

import asyncio
import aiohttp
import threading
from .websocket_event import Websocket_Event
import xml.etree.ElementTree as ET
import logging
logger = logging.getLogger(__name__)

headers = {
    "Sec-WebSocket-Protocol": "ISYSUB",
    "Origin" : "com.universal-devices.websockets.isy",
}


class Websocket_Client(object):

    def __init__(self,controller,address,port,username,password,https, **kwargs):
        self._address = address
        self._port = port
        self.controller = controller
        self._https = https
        self.auth = aiohttp.BasicAuth('admin','admin')
        
        # set some default values
        self.reply_timeout = kwargs.get('heartbeat') or 30
        self.sleep_time = kwargs.get('sleep_time') or 10

        self._connected = False

        self.connect()
    
    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self,connected):
        if self._connected != connected:
            self._connected = connected
            logger.warning ('Websocket Connected {}'.format(connected))
            if self.controller:
                self.controller.websocket_connected(connected)

    def connect(self):
        def start():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            #loop = asyncio.get_event_loop()
            loop.run_until_complete(self.listen_forever())
            loop.run_until_complete(asyncio.sleep(0))
            # Wait 250 ms for the underlying SSL connections to close
            #loop.run_until_complete(asyncio.sleep(0.250))            
            loop.close()

        logger.warning ('Starting websocket thread')
        self._ws_thread = threading.Thread(
            target=start, args=())
            
        self._ws_thread.daemon = True
        self._ws_thread.start()

    async def listen_forever(self):
        URL = "ws://"+self._address+"/rest/subscribe"
        session = None

        while True:
            # outter loop restarted every time the connection fails
            logger.warning('Outter loop...')

            if session is not None and session.closed is False:
                await session.close()

            session = aiohttp.ClientSession()

            try:
                async with session.ws_connect(URL,headers=headers,auth=self.auth,heartbeat=30) as ws:
                    logger.warning ('Waiting for messages. WS Closed {} {} Info  {}'.format(ws.closed,ws.exception(),ws.protocol))

                    async for msg in ws:
                        self.connected = True
                        #print('Message received from server:', msg)
                        logger.warning('Websocket Message: {}'.format(msg))
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

                        elif msg.type == aiohttp.WSMsgType.BINARY:
                            logger.warning ('Websocket Binary: {}'.format(msg.data))

                        elif msg.type == aiohttp.WSMsgType.PING:
                            ws.pong()

                        elif msg.type == aiohttp.WSMsgType.PONG:
                            logger.warning('Pong received')
                        
                        elif msg.type == aiohttp.WSMsgType.CLOSE:
                            logger.warning('Close received')
                            await ws.close()

                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            logger.error ('Error during receive {}'.format(ws.exception()))
                            
                        elif msg.type == aiohttp.WSMsgType.CLOSED:
                            logger.warning ('Close {}'.format(ws.exception()))
                            await ws.close()
                
                self.connected = False

                logger.warning('Aysnc loop completed. Session closed {}'.format(session.closed))
                await asyncio.sleep(self.sleep_time)
                logger.warning('Aysnc timeout finished. Session closed {}'.format(session.closed))

            except Exception as ex:
                self.connected = False
                logger.error('Websocket Error {}'.format(ex))
                await asyncio.sleep(self.sleep_time)
                continue


if __name__ == '__main__':
    try:
        wsc = Websocket_Client(False,"192.168.1.51",80,'admin','admin',False)

        while True:
            pass
           #time.sleep(10)


        #wsc.start()

    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")
