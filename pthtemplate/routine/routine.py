class Routine:
    def __init__(self):
        pass

    def apply(self, epoch, iteration, update, **kwargs):
        raise NotImplementedError
