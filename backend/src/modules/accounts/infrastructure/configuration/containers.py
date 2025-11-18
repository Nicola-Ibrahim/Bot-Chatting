from dependency_injector import containers, providers

from ..crypto.password_hasher import PBKDF2PasswordHasher
from ..mediator import Mediator
from ..messaging.email_notifier import ConsoleNotificationService
from ..persistence.repositories.sql_account_repo import SQLAccountRepository
from ..persistence.repositories.sql_role_repo import SQLRoleRepository
from ..persistence.repositories.sql_session_repo import SQLSessionRepository

handlers: dict = {}


class RepositoryDIContainer(containers.DeclarativeContainer):
    """DB + repositories wiring for Accounts BC."""

    config = providers.Configuration()

    db = providers.DependenciesContainer()  # expects: session (Factory) or session_factory

    account_repository = providers.Singleton(
        SQLAccountRepository,
        session=db.provided.session,
    )
    session_repository = providers.Singleton(
        SQLSessionRepository,
        session=db.provided.session,
    )
    role_repository = providers.Singleton(
        SQLRoleRepository,
        session=db.provided.session,
    )


class ServicesDIContainer(containers.DeclarativeContainer):
    """Cross-cutting services for Accounts BC."""

    password_hasher = providers.Singleton(PBKDF2PasswordHasher)
    notification_service = providers.Singleton(ConsoleNotificationService)


class AccountsDIContainer(containers.DeclarativeContainer):
    """Top-level Accounts BC container."""

    config = providers.Configuration()

    data = providers.Container(RepositoryDIContainer, config=config)
    services = providers.Container(ServicesDIContainer)

    mediator = providers.Singleton(Mediator, handlers=handlers)

    # Wire the application package if you use Provide[...] markers
    wiring_config = containers.WiringConfiguration(
        packages=["src.backend.modules.accounts.application"],
    )
