from collections import OrderedDict
from pprint import pprint


parser = xxx
subparsers = None
subparser = None
opts = OrderedDict()
args = None

def add_argument(*args, **kwargs):
    """both parser and subparser"""
    if subparser is None:
        parser.add_argument(*args, **kwargs)
    else:
        subparser.add_argument(*args, **kwargs)


def set_defaults(**kwargs):
    """both parser and subparser"""
    if subparser is None:
        parser.set_defaults(**kwargs)
    else:
        subparser.set_defaults(**kwargs)


def add_subparsers(*args, **kwargs):
    subparsers = parser.add_subparsers(*args, **kwargs)


class SubparserContext:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def __enter__(self):
        assert subparser is not None, 'Invalid subparser, got None'
        subparser = subparsers.add_parser(*self._args, **self._kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        subparser = None


def add_parser(*args, **kwargs):
    return SubparserContext(*args, **kwargs)


def parse_args():
    args = parser.parse_args()


def accept_argument(key, value=None):
    if value is None:
        opts[key] = getattr(args, key)
    else:
        opts[key] = value


def print_opts():
    pprint(opts)
