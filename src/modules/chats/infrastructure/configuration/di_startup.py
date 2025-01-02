from .conversation.di import ConversationDIContainer
from .downloader.di import DownloaderDIContainer
from .email.di import EmailDIContainer


class DIStartup:
    def __init__(self):
        self.conversation_container: ConversationDIContainer = ConversationDIContainer()
        self.email_container: EmailDIContainer = EmailDIContainer()
        self.downloader_container: DownloaderDIContainer = DownloaderDIContainer()

    def init_all(self) -> None:
        self.conversation_container.init_resources()
        self.email_container.init_resources()
        self.downloader_container.init_resources()

    def shutdown_all(self) -> None:
        self.conversation_container.shutdown_resources()
        self.email_container.shutdown_resources()
        self.downloader_container.shutdown_resources()
