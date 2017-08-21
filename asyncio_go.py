#!/usr/bin/env python
# encoding: utf-8

"""
@description: awesome asyncio

@author: pacman
@time: 2017/8/21 14:55
"""

import asyncio
import aiohttp
from timer import log_time

host = 'http://example.com'
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9', }

loop = asyncio.get_event_loop()


async def fetch(url):
    async with aiohttp.ClientSession(loop=loop) as sess:
        async with sess.get(url) as response:
            result = await response.read()
            return result


@log_time
def run():
    tasks = [fetch(host + url) for url in urls_todo]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    for item in results:
        print(item)


def main():
    run()


if __name__ == '__main__':
    main()
