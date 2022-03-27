from abc import abstractmethod, ABCMeta


class Relation(metaclass=ABCMeta):
    @abstractmethod
    def prepare_dataset(self):
        pass
