from abc import ABC, abstractmethod

from ..models.member_id import MemberId
from ..root import Member


class AbstractMemberRepository(ABC):
    @abstractmethod
    def save(self, member: Member) -> None:
        pass

    @abstractmethod
    def find(self, member_id: MemberId) -> Member:
        pass

    @abstractmethod
    def find_all(self, chat_id: ChatId) -> List[Member]:
        pass

    @abstractmethod
    def find_by_user(self, user_id: UserId) -> List[Member]:
        pass

    @abstractmethod
    def delete(self, member_id: MemberId) -> None:
        pass

    @abstractmethod
    def update(self, member: Member) -> None:
        pass

    @abstractmethod
    def exists(self, member_id: MemberId) -> bool:
        pass

    @abstractmethod
    def count(self, chat_id: ChatId) -> int:
        pass

    @abstractmethod
    def delete_all(self, chat_id: ChatId) -> None:
        pass
