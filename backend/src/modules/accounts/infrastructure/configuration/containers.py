from dependency_injector import containers, providers

from ..crypto.password_hasher import PBKDF2PasswordHasher
from ..mediator import Mediator
from ..messaging.email_notifier import ConsoleNotificationService
from ..persistence.repositories.sql_account_repo import SQLAccountRepository
from ..persistence.repositories.sql_role_repo import SQLRoleRepository
from ..persistence.repositories.sql_session_repo import SQLSessionRepository

handlers: dict = {}


class AccountsDIContainer(containers.DeclarativeContainer):
    """Top-level Accounts BC container."""

    config = providers.Configuration()

    session_factory = providers.Dependency()  # wired in via AccountsStartUp

    account_repository = providers.Singleton(
        SQLAccountRepository,
        session_factory=session_factory,
    )
    session_repository = providers.Singleton(
        SQLSessionRepository,
        session_factory=session_factory,
    )
    role_repository = providers.Singleton(
        SQLRoleRepository,
        session_factory=session_factory,
    )

    password_hasher = providers.Singleton(PBKDF2PasswordHasher)
    
    notification_service = providers.Singleton(ConsoleNotificationService)

    mediator = providers.Singleton(Mediator, handlers=handlers)

    wiring_config = containers.WiringConfiguration(
        packages=["src.backend.modules.accounts.application"],
    )
