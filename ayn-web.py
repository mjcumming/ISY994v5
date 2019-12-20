import asyncio
import os

import aiohttp

from base64 import b64encode

auth = b64encode(('admin'+':'+'admin').encode('UTF-8')).decode("ascii")

headers = [
    'Authorization: Basic %s' % auth, 
    "Sec-WebSocket-Protocol: ISYSUB",
    "Origin: com.universal-devices.websockets.isy"
]


URL = "ws://"+'192.168.1.51'+"/rest/subscribe"

async def main():
    session = aiohttp.ClientSession()
    async with session.ws_connect(URL=URL,headers=headers) as ws:

        await prompt_and_send(ws)
        async for msg in ws:
            print('Message received from server:', msg)
            await prompt_and_send(ws)

            if msg.type in (aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR):
                break


async def prompt_and_send(ws):
    new_msg_to_send = input('Type a message to send to the server: ')
    if new_msg_to_send == 'exit':
        print('Exiting!')
        raise SystemExit(0)
    await ws.send_str(new_msg_to_send)


if __name__ == '__main__':
    print('Type "exit" to quit')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())