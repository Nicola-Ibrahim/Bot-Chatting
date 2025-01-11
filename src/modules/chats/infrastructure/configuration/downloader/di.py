from dependency_injector import containers, providers

from ... import ConversationsDownloader


class DownloaderDIContainer(containers.DeclarativeContainer):
    conversation_download_service = providers.Singleton(ConversationsDownloader)
