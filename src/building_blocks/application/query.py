from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Generic, Protocol, TypeVar, runtime_checkable

TQueryResult = TypeVar("TQueryResult")


@dataclass(frozen=True, slots=True)
class Query:
    """Base type for queries dispatched through the application layer."""

    correlation_id: uuid.UUID = field(default_factory=uuid.uuid4)


TQuery = TypeVar("TQuery", bound=Query)


@runtime_checkable
class QueryHandler(Protocol, Generic[TQuery, TQueryResult]):
    """Protocol for query handlers."""

    def handle(self, query: TQuery) -> TQueryResult:
        ...
