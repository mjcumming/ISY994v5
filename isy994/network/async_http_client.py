import asyncio

import aiohttp
#work in progress


class HTTP_Client(object):

    def __init__(self,address,port=None,username='',password='',use_https=False):
        self._address = address
        self._port = port
        self._username = username
        self._password = password

        url = (use_https and 'https://' or 'http://') + self._address + '/rest/'  
        # add port...
        self._url = url
        self.session = None

    async def get_session(self):
        async with aiohttp.ClientSession(
                auth=aiohttp.BasicAuth('admin', 'admin')) as self.session:
            await self.fetch()

    async def request(self,path):
        if self.session is None:
            self.get_session()

        async with self.session.get(self._url + path) as resp:
            print(resp.status)
            body = await resp.text()
            print(body)


http = HTTP_Client('192.168.1.51')


loop = asyncio.get_event_loop()
loop.run_until_complete(http.request('nodes'))