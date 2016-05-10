"""
Merge Logic will be in the server

"""

import warnings


class GCounter:
    def __init__(self, name='counter', key='', count=0):
        """
        initialization - indicate server
        :param name:
        :param key:
        :param count:
        """
        self.name = name
        self.key = key
        self._counter = count

    def increment(self, val=1):
        self._counter += val

    def __add__(self, val):
        self._counter += val

    @property
    def counter(self):
        """
        Contact server, get the value
        :return: merged counter value
        """
        # temporarily return local value
        return self._counter

    @counter.setter
    def counter(self, value):
        """
        write code to do what you want when the counter value is set(when it increments)
        may want to send update to server.
        :type value: int
        :return:
        """
        if self._counter < value:
            self._counter = value
        else:
            warnings.warn('GCounter can only be incremented')
