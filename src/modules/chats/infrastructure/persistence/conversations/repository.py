from .....domain.conversations.interfaces.repository import Conversations
from .....domain.conversations.root import Conversation
from .model import ConversationDBModel


class SQLConversationRepository(Conversations):
    """
    SQL-based repository for managing Conversation entities.
    """

    def delete(self, conversation_id: str) -> None:
        """Delete a conversation by its ID."""
        conversation = ConversationDBModel.manager.get(conversation_id)
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} does not exist.")
        ConversationDBModel.manager.remove(conversation)

    def find(self, conversation_id: str) -> Conversation:
        """Find a conversation by its ID."""
        sql_conversation = ConversationDBModel.manager.get(conversation_id)

        # Map raw_conversation to conversation aggregate entity
        conversation = map_to_entity(sql_conversation)

        return conversation

    def find_all(self, user_id: str) -> list[Conversation]:
        """Find all conversations for a user."""
        return ConversationDBModel.manager.filter(user_id=user_id)

    def save(self, conversation: Conversation) -> None:
        """Save a new conversation."""

        # Map the conversation domain entity to SQLModel type data
        sql_conversation = map_to_db(conversation)

        ConversationDBModel.manager.add(sql_conversation)

    def update(self, conversation: Conversation) -> None:
        """Update an existing conversation."""
        ConversationDBModel.manager.update(conversation)

    def exists(self, conversation_id: str) -> bool:
        """Check if a conversation exists by its ID."""
        return ConversationDBModel.manager.exists(conversation_id)

    def count(self, user_id: str) -> int:
        """Count conversations for a user."""
        return len(ConversationDBModel.manager.filter(user_id=user_id))

    def delete_all(self, user_id: str) -> None:
        """Delete all conversations for a user."""
        conversations = ConversationDBModel.manager.filter(user_id=user_id)
        ConversationDBModel.manager.remove_all(conversations)

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the SQLModel instance into a dictionary representation.

        Returns:
            dict: Dictionary representation of the SQLModel instance.
        """
        return {field: getattr(self, field) for field in self.__fields__}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Model":
        """
        Converts a dictionary representation into a SQLModel instance.

        Args:
            data (dict): Dictionary with the attributes to set on the model.

        Returns:
            Model: A SQLModel instance with data populated.
        """
        return cls(**data)

    @classmethod
    def to_db_model(cls: Type[T], domain_obj: T) -> "Model":
        """
        Converts a domain model instance into a corresponding database model.

        Args:
            domain_obj (T): Domain model object to map to DB model.

        Returns:
            Model: Corresponding database model (SQLModel).
        """
        return cls(
            id=domain_obj.id,
            created_at=domain_obj.created_at,
            updated_at=domain_obj.updated_at,
        )

    @classmethod
    def from_db_model(cls: Type[T], db_model: "Model") -> T:
        """
        Converts a database model (SQLModel) instance into a corresponding domain model.

        Args:
            db_model (Model): Database model to map to domain model.

        Returns:
            T: Corresponding domain model instance.
        """
        # Convert the SQLModel to a domain model
        return domain_obj_class(
            id=db_model.id,
            created_at=db_model.created_at,
            updated_at=db_model.updated_at,
        )
