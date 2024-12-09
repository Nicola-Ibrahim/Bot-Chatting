from abc import ABC, abstractmethod


class BaseDTO(ABC):
    """
    Abstract base class for all DTOs, enforcing a standard mapping interface.
    """

    @classmethod
    @abstractmethod
    def from_domain(cls, domain_object):
        """Converts a domain object to a DTO."""
