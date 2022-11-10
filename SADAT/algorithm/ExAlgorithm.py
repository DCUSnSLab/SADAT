from abc import *

class Algorithm(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def algorithmWork(self):
        """
        구현 알고리즘 수행을 위한 함수
        """
        pass