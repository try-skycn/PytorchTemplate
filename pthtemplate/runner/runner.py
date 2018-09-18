from ..routine import Routine
from ..updater import Updater
from ..socket import Socket


class Runner:
    def __init__(self):
        self._routine_list = []
        self._updater_list = []
        self._socket_list = []

    def register(self, obj):
        if isinstance(obj, Routine):
            self._routine_list.append(obj)
        elif isinstance(obj, Updater):
            self._updater_list.append(obj)
        elif isinstance(obj, Socket):
            self._socket_list.append(obj)
        else:
            raise TypeError('Invalid type of obj to be registered, get {}.'.format(type(obj)))

    def apply(self, epoch, iteration):
        kwargs = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                kwargs[key] = value

        for routine in self._routine_list:
            routine.apply(epoch, iteration, kwargs.update, **kwargs)

        for updater in self._updater_list:
            if updater.condition(epoch, iteration):
                updater.apply(epoch, iteration, kwargs.update, **kwargs)

        for socket in self._socket_list:
            if socket.condition(epoch, iteration):
                socket.apply(epoch, iteration, **kwargs)
