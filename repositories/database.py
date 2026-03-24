from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    async def insert(self, **kwargs):
        pass

    @abstractmethod
    async def update(self, **kwargs):
        pass

    @abstractmethod
    async def delete(self, **kwargs):
        pass

    @abstractmethod
    async def get(self, **kwargs):
        pass
