import collections
import numpy as np
import torch
import torch.nn as nn
import torch.utils.data

from ..utils.misc import tuplize


class Runner:
    def __init__(self,
                 network,
                 criterion,
                 optimizer,
                 scheduler=None):
        self._convertings = {}
        self._updatings = []
        self._loggings = []
        
        self.network = network
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler

    def converting(self, key, mapping):
        self._convertings[key] = mapping

    def _converting(self, key, *args):
        return self._convertings.get(key, tuplize)(*tuplize(*args))

    def updating(self, condition, updating):
        self._updatings.append((condition, updating))

    def logging(self, condition, logging):
        self._loggings.append((condition, logging))

    def _body(self, epoch, iteration, kwargs):
        self.network.train()
        parallel = torch.cuda.is_available() and torch.cuda.device_count() > 1

        if parallel:
            network = nn.DataParallel(self.network)
        else:
            network = self.network
        
        kwargs.update(network=self.network, criterion=self.criterion)

        source = iteration.data
        source = self._converting('source', source)
        kwargs.update(source=source)

        target = source
        target = self._convertings('target', target)
        kwargs.update(target=target)

        self.optimizer.zero_grad()
        output = network(*tuplize(source))
        output = self._convertings('output', output)
        kwargs.update(output=output)

        loss = self.criterion(*tuplize(output), *tuplize(target))
        loss.backward()
        kwargs.update(loss=loss)

        torch.nn.utils.clip_grad_norm_(network.parameters(), 1)
        self.optimizer.step()
        if self.scheduler and int(iteration) == len(iteration):
            self.scheduler.step()

    def apply(self, epoch, iteration, device=None):
        kwargs = {}
        self._body(epoch, iteration, kwargs)

        for condition, updating in self._updatings:
            if condition(epoch, iteration):
                updating(epoch, iteration, kwargs.update, **kwargs)

        for condition, logging in self._loggings:
            if condition(epoch, iteration):
                logging(epoch, iteration, **kwargs)
