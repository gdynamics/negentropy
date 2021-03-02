from transcoder import Transcoder
from abc import abstractmethod

class MappedTranscoder(Transcoder):
    @property
    @abstractmethod
    def mapping(self):
        pass

    @abstractmethod
    def encode(plaintxt: str) -> str:
        pass
    
    @abstractmethod
    def decode(ciphertxt: str) -> str:
        pass
