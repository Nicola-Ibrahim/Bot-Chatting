from dependency_injector import containers, providers


class LoggingDIContainer(containers.DeclarativeContainer):
    logging = providers.Singleton(LoggingService)
