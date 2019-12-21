import asyncio

import aiohttp


async def fetch(session):
    print('Query http://httpbin.org/basic-auth/andrew/password')
    async with session.get(
            'http://192.168.1.51/rest/nodes') as resp:
        print(resp.status)
        body = await resp.text()
        print(body)


async def go():
    async with aiohttp.ClientSession(
            auth=aiohttp.BasicAuth('admin', 'admin')) as session:
        await fetch(session)


loop = asyncio.get_event_loop()
loop.run_until_complete(go())