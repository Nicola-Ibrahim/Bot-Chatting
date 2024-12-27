from .....building_blocks.domain.events import DomainEvent


class EventDispatcher:
    """
    Handles the dispatching of domain events to listeners.
    """

    def __init__(self):
        self.listeners = {}

    def register_listener(self, event_type, listener):
        """
        Registers a listener for a specific event type.
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def dispatch(self, event: DomainEvent):
        """
        Dispatches an event to the registered listeners.
        """
        for listener in self.listeners.get(type(event), []):
            listener(event)
