from abc import ABCMeta, abstractclassmethod, abstractmethod

class RadioGym(metaclass = ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def step():
        pass

    @abstractmethod
    def render():
        pass

    @abstractmethod
    def reset():
        pass

    @abstractmethod
    def action():
        pass

    @abstractmethod
    def get_states():
        pass

    @abstractmethod
    def get_reward():
        pass