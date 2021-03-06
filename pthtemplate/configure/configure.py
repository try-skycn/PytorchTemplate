import datetime
import argparse
from collections import OrderedDict
from pprint import pprint


__all__ = ['opts', 'args',
           'add_argument', 'set_defaults', 'add_subparsers',
           'add_parser', 'parse_args', 'accept_argument',
           'print_opts']


parser = argparse.ArgumentParser()
subparsers = None
subparser = None
opts = OrderedDict()
args = None


def create_parser(*pargs, **kwargs):
    global parser
    parser = argparse.ArgumentParser(*pargs, **kwargs)


def add_argument(*pargs, **kwargs):
    """both parser and subparser"""
    global parser
    global subparser
    if subparser is None:
        parser.add_argument(*pargs, **kwargs)
    else:
        subparser.add_argument(*pargs, **kwargs)


def set_defaults(**kwargs):
    """both parser and subparser"""
    global parser
    global subparser
    if subparser is None:
        parser.set_defaults(**kwargs)
    else:
        subparser.set_defaults(**kwargs)


def add_subparsers(*pargs, **kwargs):
    global subparsers
    subparsers = parser.add_subparsers(*pargs, **kwargs)


class SubparserContext:
    def __init__(self, *pargs, **kwargs):
        self._pargs = pargs
        self._kwargs = kwargs

    def __enter__(self):
        global subparsers
        global subparser
        if subparsers is None:
            subparsers = parser.add_subparsers()
        subparser = subparsers.add_parser(*self._pargs, **self._kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        global subparser
        subparser = None


def add_parser(*pargs, **kwargs):
    return SubparserContext(*pargs, **kwargs)


def parse_args(*pargs, **kwargs):
    global parser
    global args
    args = parser.parse_args(*pargs, **kwargs)


def accept_argument(key, value=None):
    global opts
    global args
    if value is None:
        opts[key] = getattr(args, key)
    else:
        opts[key] = value


def get_exp_id(exp_name=None):
    dt = datetime.datetime.now()
    exp_id = '{}_{:02d}-{:02d}-{:02d}'.format(dt.date(), dt.hour, dt.minute, dt.second)
    if exp_name is not None:
        exp_name = '{}_{}'.format(exp_id, exp_name)
    return exp_id


def print_opts():
    global opts
    pprint(opts)
