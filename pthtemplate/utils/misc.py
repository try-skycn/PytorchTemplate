def tuplize(*args):
    expanded = []
    for x in args:
        if isinstance(x, tuple) or isinstance(x, list):
            expanded.extend(x)
        else:
            expanded.append(x)
    return tuple(x)
