# 🧩 DDD Implementation Guide

This document explains how tactical Domain-Driven Design (DDD) patterns are implemented in the Horizon Chat System. We bridge the gap between high-level theory and the actual Python codebase.

---

## 🏗️ Core Building Blocks

Most domain concepts inherit from base classes located in `backend/src/building_blocks/domain/`.

### 1. Entities
Entities are objects that have a distinct identity that runs through time and different representations.
- **Implementation**: Inherit from `Entity[TEntityId]`.
- **Key Features**: 
    - Unique `id`.
    - Automatic `created_at` and `updated_at` tracking.
    - Versioning for optimistic concurrency.
    - Ability to record and pull `DomainEvents`.

```python
# Example: Participant entity in chats module
@dataclass(eq=False)
class Participant(Entity[MemberId]):
    _role: ParticipantRole
    # ...
```

### 2. Aggregate Roots
An Aggregate is a cluster of associated objects that we treat as a unit for data changes. The Aggregate Root is the only member of the aggregate that outside objects are allowed to hold a reference to.
- **Implementation**: Inherit from `AggregateRoot[TId]`.
- **Key Features**: 
    - Acts as a consistency boundary.
    - Encapsulates all state changes via methods (no public setters).
    - Enforces business rules before any state change.

```python
# Example: Conversation aggregate root
@dataclass
class Conversation(AggregateRoot[ConversationId]):
    _title: str
    _participants: list[Participant]
    
    def add_participant(self, participant_id: MemberId, role: ParticipantRole):
        self.check_rules(ParticipantCannotBeAddedIfAlreadyExistsRule(...))
        # Logic to add participant
        self.add_event(ParticipantAddedEvent(...))
```

### 3. Value Objects
Value Objects represent descriptive aspects of the domain with no identity. They are immutable.
- **Implementation**: Inherit from `ValueObject`.
- **Key Features**: 
    - Equality is based on attributes, not ID.
    - Immutable (use `replace` or `copy` to create new versions).

### 4. Business Rules
Instead of scattering `if` statements throughout the domain, we encapsulate business logic into "Rule" objects.
- **Pattern**: "Always-Valid Domain Model".
- **Implementation**: Inherit from `BaseBusinessRule`.

```python
# Example of checking a rule
def rename(self, new_title: str):
    self.check_rules(TitleCannotBeEmptyRule(new_title))
    self._title = new_title
```

---

## 🛰️ Domain Events

Domain events are "things that happened in the domain that domain experts care about". They are used to decouple different parts of the system and trigger side effects (like sending notifications).

1. **Recording**: An Aggregate Root records an event during a command (e.g., `self.add_event(...)`).
2. **Dispatching**: After the transaction is committed, the `UnitOfWork` or `Repository` pulls these events and dispatches them via a `Mediator`.
3. **Handling**: Event Handlers in other modules (or the same module) react to these events.

---

## 🧪 Consistency & Validation

We follow the **Always-Valid** principle:
- An object cannot be created in an invalid state.
- A method cannot leave an object in an invalid state.
- Validation happens *inside* the domain layer using Business Rules, not just at the API boundary.

---

## 📂 Mapping Theory to Code

| DDD Concept | Code Location |
| :--- | :--- |
| **Bounded Context** | `backend/src/modules/<module_name>/` |
| **Shared Kernel** | `backend/src/building_blocks/` |
| **Aggregate Root** | `.../domain/<context>/<aggregate>.py` |
| **Domain Service** | `.../domain/services/` |
| **Repository Interface** | `.../domain/interfaces/` |
| **Repository Impl** | `.../infrastructure/repositories/` |
| **Application Module** | `.../application/commands/` or `.../queries/` |
