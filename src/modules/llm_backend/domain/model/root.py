from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Self
from uuid import uuid4

from src.building_blocks.domain.aggregate_root import AggregateRoot
from src.building_blocks.domain.events import ModelInteractionCreatedEvent

from .value_objects.interaction_id import InteractionId
from .value_objects.metadata import Metadata
from .value_objects.query import Query
from .value_objects.reponse import Response


@dataclass
class ModelInteraction(AggregateRoot):
    _id: InteractionId
    _model_name: ModelName
    _user_id: UserId
    _query: Query
    _response: Response
    _metadata: dict = field(default_factory=dict)

    @property
    def model_name(self) -> ModelName:
        return self._model_name

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def query(self) -> Query:
        return self._query

    @property
    def response(self) -> Response:
        return self._response

    @property
    def metadata(self) -> Metadata:
        return Metadata(self._metadata)

    @classmethod
    def create(
        cls,
        model_name: ModelName,
        user_id: UserId,
        query: Query,
        response: Response,
        metadata: Metadata | None = None,
    ) -> Self:
        interaction = cls(
            _id=InteractionId.create(id=uuid4()),
            _model_name=model_name,
            _user_id=user_id,
            _query=query,
            _response=response,
        )

        interaction.add_event(
            ModelInteractionCreatedEvent(
                interaction_id=interaction.id,
                model_name=model_name,
                user_id=user_id,
                timestamp=interaction.timestamp,
            )
        )
        return interaction
