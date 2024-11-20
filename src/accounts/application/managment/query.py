from typing import Callable

from ...domain.model.root_entity import User
from ...domain.model.exceptions import UserNotFoundError


class UserQueryUseCase:
    def __init__(self, user_repo: IUserRepository, db_session: Callable[[], ContextManager[Session]]) -> None:
        self.user_repo = user_repo
        self.db_session = db_session

    def get_user(self, user_id: int):

        with self.db_session() as session:
            user: User | None = self.user_repo.find_user_by_id(session=session, user_id=user_id)

        if user is None:
            raise UserNotFoundError()

        return user
