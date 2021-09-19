from abc import ABCMeta, abstractmethod


class Tank:
    __metaclass__ = ABCMeta

    # @abstractmethod
    # def move(self):
    #     """ Начать движение """
    #
    # @abstractmethod
    # def update_position(self):
    #     """ Изменить позицию, если это возможно """

    @abstractmethod
    def shoot(self, level, global_timer):
        """ Выстрелить """
