class Updater:
    def __init__(self):
        pass

    def condition(self, epoch, iteration):
        raise NotImplementedError

    def apply(self, epoch, iteration, update, **kwargs):
        raise NotImplementedError
