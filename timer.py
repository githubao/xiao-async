#!/usr/bin/env python
# encoding: utf-8

"""
@description: 

@author: BaoQiang
@time: 2017/8/21 13:22
"""

import functools
import time
import logging


def log_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tick = time.time()
        logging.error('@{}， {{{}}} start'.format(time.strftime('%X', time.localtime()), func.__name__))
        res = func(*args, **kwargs)
        logging.error('@{}， {{{}}} end'.format(time.strftime('%X', time.localtime()), func.__name__))
        logging.error('@{:.3f}s， taken for {}'.format(time.time() - tick, func.__name__))

        return res

    return wrapper