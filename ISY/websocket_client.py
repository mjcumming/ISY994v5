

#!/usr/local/bin/python

import websocket
import threading
from base64 import b64encode
import logging
import time

import xml.etree.ElementTree as ET

from isy_event import ISY_Event

logger = logging.getLogger(__name__)

class Websocket_Client(object):

    def __init__(self,address,port,username,password,https,callback):
        self._address = address
        self._port = port

        self._auth = b64encode((username+':'+password).encode('UTF-8')).decode("ascii")

        self._https = https
        self._callback = callback 

        self._headers = [
            'Authorization: Basic %s' % self._auth, 
            "Sec-WebSocket-Protocol: ISYSUB",
            "Origin: com.universal-devices.websockets.isy"
        ]

        self.connect()

    def connect(self):
        self.connected = False

        self._ws = websocket.WebSocketApp(
            "ws://"+self._address+"/rest/subscribe",
            header=self._headers,
            on_open = lambda ws : self._on_open (ws),
            on_message = lambda ws,message : self._on_message (ws,message),
            on_error = lambda ws,err : self._on_error (ws,err),
            on_close = lambda ws : self._on_close (ws),
        )
        
        self._ws_thread = threading.Thread(
            target=self._ws.run_forever, args=())
            
        self._ws_thread.daemon = True
        self._ws_thread.start()
        
    def _on_open(self,ws):
        logger.info('Connected')
        self.connected = True

    def _on_message(self,ws, message):
        logger.info('Message: {}'.format(message))
        #print('message',message)

        event = ISY_Event(message)

        if event.node is not None: #event from a device node
            #print ('device event')
            if event.control == 'ST':
                print ('device {}. changed status to {}'.format(event.node,event.action))
            elif event.control in ['DON','DOF']:
                print ('device {}. changed local control {}'.format(event.node,event.action))

        '''
        print (root.text)
        control = root.find('control')
        action = root.find ('action')

        print ('control:action',control.text,action.text)

        if control.text == '_1':
            action = root.find('action')
            event_info = root.find('eventInfo')

            print('event info',event_info.text)

            #event.find("eventInfo").text[1:13].strip()
'''
    def _on_error(self,ws, error):
        logger.error('Error: {}'.format(error))
        print('error',error)

    def _on_close(self,ws):
        logger.info('Disonnected')
        self.connected = False
        self.connect()




if __name__ == "__main__":
    websocket.enableTrace(True)

    try:
        wsc = Websocket_Client("192.168.1.213",80,'admin','admin',False,None)

        while True:
            time.sleep(2)

    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")

