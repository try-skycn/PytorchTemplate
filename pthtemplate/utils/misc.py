import os


def tuplize(*args):
    expanded = []
    for x in args:
        if isinstance(x, tuple) or isinstance(x, list):
            expanded.extend(x)
        else:
            expanded.append(x)
    return tuple(x)

def mkdir_p(path):
    import errno
    try:
        os.makedirs(path)
        print('Created directory {}'.format(path))
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            print('Directory {} already exists.'.format(path))
        else:
            raise
