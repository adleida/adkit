#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    adkit.utils
    ~~~~~~~~~~~
    This module implements the utils
'''

import functools
import io
import json
import jsonschema
import os.path
import pkgutil
import requests
import yaml
import types
import time


@functools.lru_cache()
def load_schema(name):

    name = '{}-schema.json'.format(name)
    obj = load_resource(name)
    schema = jsonschema.Draft4Validator(obj)
    return schema


@functools.lru_cache()
def load_resource(name, as_object=True):

    path = 'res/{}'.format(name)
    blob = pkgutil.get_data(__package__, path)
    if blob == None:
        raise Exception('no such resource: {}'.format(name))
    data = blob.decode()
    if as_object:
        ext = os.path.splitext(name)[-1]
        if ext in ['.json']:
            data = json.loads(data)
        elif ext in ['.yaml', '.yml']:
            data = yaml.load(io.StringIO(data))
        else:
            raise Exception('cannot detect resource type')
    return data


def check_schema(obj, schema):

    try:
        schema = load_schema(schema)
        schema.validate(obj)
        return True, None
    except Exception as ex:
        return False, Exception(ex.message)


def load_json(data):

    return json.loads(data)


def dump_json(data):

    return json.dumps(data, indent=2, ensure_ascii=False)


def wget_obj(url):

    if os.path.exists(url):
        _, ext = os.path.splitext(url)
        if ext in ['.json']:
            return json.load(open(url))
        elif ext in ['.yaml', '.yml']:
            return yaml.load(open(url))
        else:
            raise Exception('cannot detect resource type')
    else:
        return requests.get(url, timeout=3).json()


def load_conf(fname):

    if os.path.exists(fname):
        _, ext = os.path.splitext(fname)
        if ext in ['.json']:
            return json.load(open(fname))
        elif ext in ['.yaml', '.yml']:
            return yaml.load(open(fname))
        else:
            raise Exception('cannot detect resource type')
    else:
        raise Exception('config file not found')


def update_request(cfg):

    for dp in cfg.get('dsp').get('s'):
        nf = dp.get('notice_file')
        rf = dp.get('res_file')
        if isinstance(nf, str) and os.path.exists(nf):
            dp['notice_file'] = load_conf(nf) 
        if isinstance(rf, str) and os.path.exists(rf):
            dp['res_file'] = load_conf(rf) 

    return cfg


def load_file(fname):
    with open(fname) as f:
        return json.loads(f.read())


class MyError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "The error message is %s" % self.message


def compare_dictionaries(dict1, dict2):

    '''cmp dict'''
    dicts_are_equal = True
    for key in dict2.keys():
        if type(dict2[key]) is dict:
            dicts_are_equal = dicts_are_equal and compare_dictionaries(dict1[key], dict2[key])
        else:
            dicts_are_equal = dicts_are_equal and (dict1[key] == dict2[key])
            if not dicts_are_equal:
                raise MyError("The key %s of dict1 not equeal dict2" % key)

    return dicts_are_equal

