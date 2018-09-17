class EpochObject(object):
    def __init__(self, epoch, length):
        super(EpochObject, self).__init__()

        self._epoch = epoch
        self._length = length

    def __int__(self):
        return self._epoch

    def __len__(self):
        return self._length


class Epoch(object):
    def __init__(self, length):
        self._length = length

    def __iter__(self):
        for i in range(self._length):
            yield EpochObject(i+1, self._length)
