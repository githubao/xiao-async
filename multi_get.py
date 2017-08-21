#!/usr/bin/env python
# encoding: utf-8

"""
@description: 几种不同的异步方式的测试对比

@author: BaoQiang
@time: 2017/8/21 13:18
"""

from timer import log_time
import socket
from concurrent import futures


def blocking_way():
    sock = socket.socket()
    sock.connect(('example.com', 80))
    request = 'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        chunk = sock.recv(4096)

    return response


def sync_way():
    res = []
    for i in range(10):
        res.append(blocking_way())
    return res


@log_time
def process_way():
    """
    ERROR:root:@6.849s， taken for process_way
    :return: 
    """
    workers = 10

    with futures.ProcessPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for _ in range(10)}

    return list(fut.result() for fut in futs)


@log_time
def thread_way():
    """
    ERROR:root:@4.226s， taken for thread_way
    :return: 
    """
    workers = 10

    with futures.ThreadPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for _ in range(10)}

    return list(fut.result() for fut in futs)

def noblocking_way():
    sock = socket.socket()
    sock.setblocking(False)

    try:
        sock.connect(('example.com',80))
    except BlockingIOError:
        pass

    request = 'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n'
    data = request.encode('ascii')
    while True:
        try:
            sock.send(data)
            break
        except OSError:
            pass

    response = b''
    while True:
        try:
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                chunk = sock.recv(4096)
            break
        except OSError:
            pass

    return response

def async_way():
    res = []
    for i in range(10):
        res.append(noblocking_way())
    return res

def run():
    # print(sync_way())
    print(process_way())
    print(thread_way())


def main():
    run()


if __name__ == '__main__':
    main()
