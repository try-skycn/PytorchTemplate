from .runner import Runner


class EvalRunner(Runner):
    """
    A runner that sequentially executes procedures for evaluation of a trained network.
    """
    def __init__(self, network):
        super().__init__()
        self.network = network
