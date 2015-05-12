#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import requests
import os


class Client(object):

    def __init__(self, url=None):
        self.req = None
        self.res = None
        self.url = url
        self.headers = {}

    def set_headers(self, **kwargs):
        self.headers.update(kwargs)

    def get_data(self, **kwargs):
        try:
            self.res = requests.get(self.url, **kwargs)
        except Exception as ex:
            pass

    def post_json_data(self, json=None, **kwargs):
        try:
            self.res = requests.post(self.url, json=json, **kwargs)
        except Exception as ex:
            pass

    def post_normal_data(self, data=None, **kwargs):
        try:
            self.res = requests.post(self.url, data=data, **kwargs)
        except Exception as ex:
            pass
