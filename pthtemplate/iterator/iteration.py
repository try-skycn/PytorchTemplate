class IterationObject(object):
    def __init__(self, epoch, iteration, length, **kwargs):
        self._epoch = epoch
        self._iteration = iteration
        self._length = length
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __int__(self):
        return self._iteration

    def __len__(self):
        return self._length

    @property
    def global_step(self):
        return self._length * (int(self._epoch) - 1) + self._iteration
    


class Iteration(object):
    def __init__(self, epoch, **kwargs):
        super(Iteration, self).__init__()

        self._epoch = epoch
        items = list(kwargs.items())
        self._keys = [k for k, _ in items]
        self._iterators = [v for _, v in items]
        self._length = None
        for iterator in self._iterators:
            try:
                length = len(iterator)
                if self._length is None or length < self._length:
                    self._length = length
            except TypeError:
                pass

    def __iter__(self):
        for i, values in enumerate(zip(*self._iterators)):
            kwargs = {k: v for k, v in zip(self._keys, values)}
            yield IterationObject(self._epoch, i+1, self._length, **kwargs)
