import os
import shutil


def tuplize(*args):
    expanded = []
    for x in args:
        if isinstance(x, tuple) or isinstance(x, list):
            expanded.extend(x)
        else:
            expanded.append(x)
    return tuple(expanded)

def mkdir_p(path, clear=False):
    if os.path.exists(path):
        if os.path.isdir(path):
            if clear:
                shutil.rmtree(path)
                os.makedirs(path)
                print('Directory {} recreated.'.format(path))
            else:
                print('Directory {} already exists.'.format(path))
        else:
            raise OSError('Path {} is not a directory.'.format(path))
    else:
        os.makedirs(path)
        print('Created directory {}'.format(path))
