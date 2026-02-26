from src.modules.chats.infrastructure.configuration.startup import ChatsStartUp


def test_chat_services_are_registered_and_resolvable():
    startup = ChatsStartUp()
    startup.initialize(database_url="sqlite:///:memory:", max_active_chats_per_user=5)

    container = startup.container

    lifecycle_svc = container.conversation_lifecycle_service()
    membership_svc = container.membership_service()
    messaging_svc = container.messaging_service()
    query_svc = container.chat_query_service()

    assert lifecycle_svc is not None
    assert membership_svc is not None
    assert messaging_svc is not None
    assert query_svc is not None

    startup.stop()
