import logging

from dependency_injector import containers, providers


class LoggerDIContainer(containers.DeclarativeContainer):
    logger = providers.Singleton(logging.getLogger, name="chat")
