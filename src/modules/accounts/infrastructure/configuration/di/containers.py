from dependency_injector import containers, providers

from ...crypto.password_hasher import PBKDF2PasswordHasher
from ...messaging.email_notifier import ConsoleNotificationService
from ...persistence.repositories.sql_account_repo import SQLAccountRepository
from ...persistence.repositories.sql_role_repo import SQLRoleRepository
from ...persistence.repositories.sql_session_repo import SQLSessionRepository


class RepositoryDIContainer(containers.DeclarativeContainer):
    database = providers.DependenciesContainer()

    account_repository = providers.Singleton(
        SQLAccountRepository,
        session_factory=database.session_factory,
    )
    session_repository = providers.Singleton(
        SQLSessionRepository,
        session_factory=database.session_factory,
    )
    role_repository = providers.Singleton(
        SQLRoleRepository,
        session_factory=database.session_factory,
    )


class DataAccessDIContainer(containers.DeclarativeContainer):
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

    data = providers.Container(DataAccessDIContainer, config=config)
    services = providers.Container(ServicesDIContainer)

    # Application service wiring
    accounts_service = providers.Factory(
        AccountsService,
        account_repository=data.provided.account_repository,
        session_repository=data.provided.session_repository,
        role_repository=data.provided.role_repository,
        password_hasher=services.provided.password_hasher,
        notification_service=services.provided.notification_service,
    )

    # Wire the application package if you use Provide[...] markers
    wiring_config = containers.WiringConfiguration(
        packages=["src.contexts.accounts.application"],
    )
