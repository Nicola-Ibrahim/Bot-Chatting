from dependency_injector import containers, providers

from ...application.access_control.service import AccessControlService
from ...application.account.service import AccountService
from ...application.authentication.service import AuthenticationService
from ...application.registration.service import RegistrationService
from ..crypto.password_hasher import PBKDF2PasswordHasher
from ..messaging.email_notifier import ConsoleNotificationService
from ..persistence.repositories.sql_account_repo import SQLAccountRepository
from ..persistence.repositories.sql_role_repo import SQLRoleRepository
from ..persistence.repositories.sql_session_repo import SQLSessionRepository


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

    token_factory = providers.Dependency()

    account_service = providers.Factory(
        AccountService,
        account_repository=account_repository,
        password_hasher=password_hasher,
    )

    authentication_service = providers.Factory(
        AuthenticationService,
        account_repository=account_repository,
        session_repository=session_repository,
        password_hasher=password_hasher,
        token_factory=token_factory,
    )

    registration_service = providers.Factory(
        RegistrationService,
        account_repository=account_repository,
        password_hasher=password_hasher,
        notification_service=notification_service,
    )

    access_control_service = providers.Factory(
        AccessControlService,
        account_repo=account_repository,
        role_repo=role_repository,
    )

    wiring_config = containers.WiringConfiguration(
        packages=["src.modules.accounts.application"],
    )
