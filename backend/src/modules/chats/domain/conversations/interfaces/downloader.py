from abc import ABC, abstractmethod


class AbstractConversationDownloader(ABC):
    @abstractmethod
    def download():
        raise NotImplementedError
