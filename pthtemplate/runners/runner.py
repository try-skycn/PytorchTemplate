import collections

from ..utils.misc import tuplize


class Runner:
    def __init__(self):
        self._convertings = collections.defaultdict(lambda: tuplize)
        self._updatings = []
        self._loggings = []

    def converting(self, key, mapping):
        """
        Set a converting when "key" is activated.
        "mapping" should only accept positional arguments.
        """
        self._convertings[key] = mapping

    def updating(self, condition, updating):
        """
        Set an "updating" with "condition".
        """
        self._updatings.append((condition, updating))

    def logging(self, condition, logging):
        """
        Set an "logging" with "condition"
        """
        self._loggings.append((condition, logging))

    def _body(self, epoch, iteration, kwargs):
        raise NotImplementedError

    def apply(self, epoch, iteration, device=None):
        kwargs = {}
        self._body(epoch, iteration, kwargs)

        for condition, updating in self._updatings:
            if condition(epoch, iteration):
                updating(epoch, iteration, kwargs.update, **kwargs)

        for condition, logging in self._loggings:
            if condition(epoch, iteration):
                logging(epoch, iteration, **kwargs)
