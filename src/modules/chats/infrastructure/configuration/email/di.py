from dependency_injector import containers, providers

from ... import EmailSender

class EmailDIContainer(containers.DeclarativeContainer):
    email_sender = providers.Singleton(EmailSender)
