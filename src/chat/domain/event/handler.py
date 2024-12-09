from .message import MessageAddedEvent


class MessageAddedEventHandler:
    def handle(self, event: MessageAddedEvent):
        """
        Handle the MessageAddedEvent and trigger any necessary side effects.
        """
        print(f"Message {event.message_id} added to conversation {event.conversation_id}")
        # Perform any necessary actions here, like sending notifications
        self._send_notification(event)

    def _send_notification(self, event: MessageAddedEvent):
        """
        Send a notification after the message has been added.
        """
        print(f"Sending notification: New message added to conversation {event.conversation_id}")
