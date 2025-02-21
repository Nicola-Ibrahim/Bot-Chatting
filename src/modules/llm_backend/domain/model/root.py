@dataclass
class ModelInteraction(AggregateRoot):
    """
    Represents an interaction with a model by a user.
    """

    _id: UUID
    _model_name: str  # Name of the model used
    _user_id: UUID
    _input_text: str
    _response_text: str
    _tokenization_id: Optional[UUID] = None
    _timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _metadata: dict = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        model_name: str,
        user_id: UUID,
        input_text: str,
        response_text: str,
        tokenization_id: Optional[UUID] = None,
        metadata: Optional[dict] = None,
    ) -> "ModelInteraction":
        """
        Factory method to create a new model interaction.
        """
        # Validate business rules
        cls.check_rules(
            InputTextMustBeValidRule(text=input_text),
            ResponseTextMustBeValidRule(text=response_text),
        )

        # Create the interaction
        interaction = cls(
            _id=uuid4(),
            _model_name=model_name,
            _user_id=user_id,
            _input_text=input_text,
            _response_text=response_text,
            _tokenization_id=tokenization_id,
            _metadata=metadata or {},
        )

        # Emit a domain event
        interaction.add_event(
            ModelInteractionCreatedEvent(
                interaction_id=interaction.id,
                model_name=model_name,
                user_id=user_id,
                timestamp=interaction.timestamp,
            )
        )

        return interaction
