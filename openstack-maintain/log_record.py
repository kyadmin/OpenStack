#!/usr/bin/env python
# coding=utf-8
# created by hansz
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='openstack_start.log',
                filemode='a+')


def error_logging(msg):
    logging.error(msg)