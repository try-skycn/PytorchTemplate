class IterationObject(object):
    def __init__(self, iteration, niterations, data):
        super(IterationObject, self).__init__()

        self.iteration = iteration
        self.niterations = niterations
        self.data = data

    def __int__(self):
        return self.iteration

    def __len__(self):
        return self.niterations

    def __repr__(self):
        keymap = ', '.join(["{}={}".format(key, repr(value)) for key, value in self.__dict__.items()
                            if key not in {"iteration", "niterations"}])
        return 'Iter({}/{}, {})'.format(self.iteration, self.niterations, keymap)

    @property
    def batch_size(self):
        return len(self.data)


class Iteration(object):
    def __init__(self, dataloader):
        super(Iteration, self).__init__()

        self.dataloader = dataloader
        self.niterations = len(dataloader)

    def __iter__(self):
        for i, data in enumerate(self.dataloader):
            yield IterationObject(iteration=i+1, data=data, niterations=self.niterations)
