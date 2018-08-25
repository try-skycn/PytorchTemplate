class EpochObject(object):
    def __init__(self, epoch, nepochs):
        super(EpochObject, self).__init__()

        self.epoch = epoch
        self.nepochs = nepochs

    def __int__(self):
        return self.epoch

    def __len__(self):
        return self.nepochs


class Epoch(object):
    def __init__(self, nepochs):
        super(Epoch, self).__init__()

        self.nepochs = nepochs

    def __iter__(self):
        for i in range(self.nepochs):
            yield EpochObject(epoch=i+1, nepochs=self.nepochs)
