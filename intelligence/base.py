from abc import ABC, abstractmethod


class IntelligenceProvider(ABC):
    """
    Base class for all threat intelligence providers.
    """

    @abstractmethod
    def lookup(self, indicator: str) -> dict:
        """
        Perform a lookup on the given indicator.
        """
        pass