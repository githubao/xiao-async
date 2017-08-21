#!/usr/bin/env python
# encoding: utf-8

"""
@description: yield from 语法

@author: pacman
@time: 2017/8/21 14:47
"""

import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from timer import log_time

from coroutine_impl import Task

selector = DefaultSelector()
stopped = False
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9', }


class Future:
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)

    def __iter__(self):
        yield self
        return self.result


def connect(sock, address):
    f = Future()
    sock.setblocking(False)
    try:
        sock.connect(address)
    except BlockingIOError:
        pass

    def on_connected():
        f.set_result(None)

    selector.register(sock.fileno(), EVENT_WRITE, on_connected)
    yield from f
    selector.unregister(sock.fileno())


def read(sock):
    f = Future()

    def on_readable():
        f.set_result(sock.recv(4096))

    selector.register(sock.fileno(), EVENT_READ, on_readable)
    chunk = yield from f
    selector.unregister(sock.fileno())
    return chunk


def read_all(sock):
    response = []
    chunk = yield from read(sock)
    while chunk:
        response.append(chunk)
        chunk = yield from read(sock)

    return b''.join(response)


class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        global stopped
        sock = socket.socket()
        yield from connect(sock, ('example.com', 80))
        get = 'GET {} HTTP/1.0\r\nHost: example.com\r\n\r\n'.format(self.url)
        sock.send(get.encode('ascii'))
        self.response = yield from read_all(sock)
        print(self.response)

        urls_todo.remove(self.url)
        if not urls_todo:
            stopped = True


def gen_parent():
    yield from gen_one()


def gen_one():
    subgen = range(10)
    yield from subgen


def gen_two():
    subgen = range(10)
    for item in subgen:
        yield item

def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()

@log_time
def yieldfrom_way():
    for url in urls_todo:
        crawler = Crawler(url)
        Task(crawler.fetch())

    loop()


def run():
    # print(list(gen_parent()))
    yieldfrom_way()


def main():
    run()


if __name__ == '__main__':
    main()
