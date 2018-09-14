from .runner import Runner


class SeqRunner(Runner):
    """
    A runner that sequentially executes procedures.
    """
    def __init__(self, network, criterion, optimizer, scheduler=None):
        super().__init__()
        self.network = network
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
