#!/usr/local/bin/python

import asyncio
import aiohttp
import functools
from .websocket_event import Websocket_Event
import xml.etree.ElementTree as ET
import logging
import time
logger = logging.getLogger(__name__)

ws_headers = {
    "Sec-WebSocket-Protocol": "ISYSUB",
    "Origin" : "com.universal-devices.websockets.isy",
}

http_headers = {
    "Connection" : "keep-alive",
}


class Async_Session(object):

    def __init__(self,controller,address,port,username,password,https=False,loop=False, **kwargs):
        self.controller = controller

        self._address = address
        self._port = port
        self._https = https

        self.loop=loop

        # set some default values
        self.reply_timeout = kwargs.get('heartbeat') or 30
        self.sleep_time = kwargs.get('sleep_time') or 5

        self._websocket_connected = False
        self._http_connected = False

        self.session=None
        self.auth = aiohttp.BasicAuth(username,password)
        self.timeout = aiohttp.ClientTimeout(total=60,connect=60,sock_connect=60,sock_read=60)
        self.loop.run_until_complete(self.create_new_session())
        #self.session = aiohttp.ClientSession(auth=self.auth,raise_for_status=True)

        self.keep_listening = True
        
    @property
    def websocket_connected(self):
        return self._websocket_connected

    @websocket_connected.setter
    def websocket_connected(self,connected):
        if self._websocket_connected != connected:
            self._websocket_connected = connected
            logger.warning ('Websocket Connected {}'.format(connected))
            if self.controller:
                wrapped = functools.partial(self.controller.websocket_connected,connected)
                self.loop.call_soon (wrapped)

    @property
    def http_connected(self):
        return self._http_connected

    @http_connected.setter
    def http_connected(self,connected):
        if self._http_connected != connected:
            self._http_connected = connected
            logger.warning ('HTTP Connected {}'.format(connected))
            if self.controller:
                wrapped = functools.partial(self.controller.http_connected,connected)
                self.loop.call_soon (wrapped)

    async def create_new_session(self):
        if self.session is not None and self.session.closed is False:
            await self.session.close()
        
        self.session = aiohttp.ClientSession(auth=self.auth,raise_for_status=True,headers=http_headers,timeout=self.timeout)

    async def request_async(self,path,timeout=10):
        if self.session is None:
            await self.create_new_session()

        logger.warning ('HTTP Get to {}'.format ('http://'+self._address+'/rest/'+path))

        try:
            async with self.session.get('http://'+self._address+'/rest/'+path,chunked=True,timeout=timeout) as response:
                if response.status == 200:
                    self.http_connected = True
                    body = await response.text()
                    #print(body)        
                    return True,body
                else:
                    self.http_connected = False
                    return False, None

        except Exception as ex:
            self.http_connected = False
            logger.error('HTTP Get Error {}'.format(ex))
            return False, None

    def request (self,path,timeout):
        try:
            future = asyncio.run_coroutine_threadsafe(self.request_async(path,timeout),self.loop)
            return future.result(10)
        except Exception as ex:
            logger.error('HTTP Get Error {}'.format(ex))
            return False, None

    def start_websocket(self):
        self.websocket_task = self.loop.create_task(self.listen_forever())

    async def listen_forever(self):
        URL = "ws://"+self._address+"/rest/subscribe"

        while self.keep_listening:
            # outter loop restarted every time the connection fails
            logger.warning('Connecting to WebSocket')

            try:
                async with self.session.ws_connect(URL,headers=ws_headers,auth=self.auth,heartbeat=30,receive_timeout=60) as ws:
                    logger.warning ('Websocket waiting for messages')

                    async for msg in ws:
                        self.websocket_connected = True
                        #print('Message received from server:', msg)
                        logger.debug('Websocket Message: {}'.format(msg))
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            try:
                                event_node = ET.fromstring (msg.data)        
                                
                                if event_node.tag == 'Event':
                                    event = Websocket_Event(event_node)

                                    if event.valid:
                                        logger.debug ('Websocket Event {}'.format(event))
                                        if self.controller:
                                            wrapped = functools.partial(self.controller.websocket_event,event)
                                            self.loop.call_soon (wrapped)
                            
                            except Exception as ex:
                                logger.error('Websocket Message Error {}'.format(ex))

                        elif msg.type == aiohttp.WSMsgType.BINARY:
                            logger.warning ('Websocket Binary: {}'.format(msg.data))

                        elif msg.type == aiohttp.WSMsgType.PING:
                            logger.warning('Ping received')
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
                
                self.websocket_connected = False

                logger.warning('Aysnc loop completed.')
                await asyncio.sleep(self.sleep_time)

            except Exception as ex:
                self.websocket_connected = False
                logger.error('Websocket Error {}'.format(ex))
                await asyncio.sleep(self.sleep_time)
                continue

            if self.keep_listening:
                await asyncio.sleep(self.sleep_time)
                await self.create_new_session()

    def close(self):
        self.keep_listening=False
        self.websocket_task.cancel()
        self.loop.run_until_complete(self.websocket_task)

        if self.session is not None and self.session.closed is False:
            self.loop.run_until_complete (self.session.close())

if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    wsc = Async_Session(False,"192.168.1.51",80,'admin','admin',False,loop=event_loop)

    try:
        wsc.start_websocket()
        event_loop.run_forever()
    
    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")
        wsc.close()
        
    finally:
        event_loop.close()
