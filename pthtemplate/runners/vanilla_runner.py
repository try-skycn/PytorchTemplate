import torch
import torch.nn as nn

from .runner import Runner


class VanillaRunner(Runner):
    def __init__(self,
                 network,
                 criterion,
                 optimizer,
                 scheduler=None):
        super(VanillaRunner, self).__init__()
        self.network = network
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler

    def _body(self, epoch, iteration, update, **kwargs):
        self.network.train()
        parallel = torch.cuda.is_available() and torch.cuda.device_count() > 1

        if parallel:
            network = nn.DataParallel(self.network)
        else:
            network = self.network
        
        update(network=self.network, criterion=self.criterion)

        source = iteration.data
        source = self.convertings['source'](source)
        update(source=source)

        target = source
        target = self.convertings['target'](target)
        update(target=target)

        self.optimizer.zero_grad()
        output = network(*tuplize(source))
        output = self.convertings['output'](output)
        update(output=output)

        loss = self.criterion(*tuplize(output), *tuplize(target))
        loss.backward()
        update(loss=loss)

        torch.nn.utils.clip_grad_norm_(network.parameters(), 1)
        self.optimizer.step()
        if self.scheduler and int(iteration) == len(iteration):
            self.scheduler.step()
