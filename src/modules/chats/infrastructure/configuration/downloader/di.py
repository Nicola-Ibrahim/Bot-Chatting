from dependency_injector import containers, providers

from ... import ConversationDownloader


class DownloaderDIContainer(containers.DeclarativeContainer):
    conversation_download_service = providers.Singleton(ConversationDownloader)
