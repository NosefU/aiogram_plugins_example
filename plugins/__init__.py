from abc import ABC, abstractmethod

from aiogram import Dispatcher


class Plugin(ABC):
    @staticmethod
    @abstractmethod
    def init(dp: Dispatcher):
        pass
