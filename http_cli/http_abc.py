from abc import ABC, abstractmethod
from typing import Self


class HttpAbc(ABC):
    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def from_bytes(cls, binary_data: bytes) -> Self:
        pass
