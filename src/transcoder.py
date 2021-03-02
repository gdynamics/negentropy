from abc import ABC, abstractmethod

class Transcoder(ABC):
    @abstractmethod
    def encode(plaintxt: str) -> str:
        pass

    @abstractmethod
    def decode(ciphertxt: str) -> str:
        pass
