# DDD Resources

Curated references for learning and applying Domain-Driven Design (DDD).

## DDD overview

Domain-Driven Design is a way to build software by modeling it around the business domain. The main goal is to keep the model and language used by the code aligned with how domain experts describe the problem. In practice, this leads to clearer boundaries, better maintainability, and fewer accidental couplings between unrelated parts of the system.

Key ideas:

- Ubiquitous language: shared vocabulary between developers and domain experts, used in code and documentation.
- Bounded contexts: explicit boundaries where a specific model applies; reduces ambiguity and prevents model conflicts.
- Aggregates: consistency boundaries that group entities and value objects and define how changes are made safely.
- Entities and value objects: entities have identity and lifecycle; value objects are immutable and defined by their attributes.
- Domain events: meaningful facts about something that happened in the domain, used to decouple workflows.
- Repositories and factories: patterns to load and create aggregates without leaking persistence concerns.

In this project, DDD shows up in feature modules (bounded contexts like auth and chat), a core layer that holds domain concepts, and application services that orchestrate use cases without mixing infrastructure details into the domain.

## Foundational concepts

1. Eric Evans: *Domain-Driven Design: Tackling Complexity in the Heart of Software*
2. [Herberto Graca on DDD](https://herbertograca.com/2017/09/07/domain-driven-design/)
3. [Always-Valid Domain Model](https://vkhorikov.medium.com/always-valid-domain-model-706e5f3d24b0)

## Architectural patterns and best practices

1. [Onion Architecture](https://medium.com/expedia-group-tech/onion-architecture-deed8a554423)
2. [Clean Domain-Driven Design](https://medium.com/unil-ci-software-engineering/clean-domain-driven-design-2236f5430a05)
3. [Clean Architecture with .NET](https://code-maze.com/dotnet-clean-architecture/)
4. [DDD and Hexagonal Architecture](https://vaadin.com/blog/ddd-part-3-domain-driven-design-and-the-hexagonal-architecture)
5. [Clean Architecture by Examples](https://github.com/amantinband/clean-architecture)

## Implementation patterns and techniques

1. [DDD Domain Models, Ports, Adapters, and CQRS](https://medium.com/vx-company/implementing-dddomain-models-ports-adapters-and-cqrs-with-c-2b81403f09f7)
2. [Ports and CQRS reference architecture](https://abstarreveld.medium.com/dddomain-models-ports-adapters-and-cqrs-reference-architecture-c-504817df65ec)
3. [Aggregate design](https://medium.com/ssense-tech/ddd-beyond-the-basics-mastering-aggregate-design-26591e218c8c)
4. [Clean DDD lessons on use cases](https://medium.com/unil-ci-software-engineering/clean-ddd-lessons-use-cases-e9d11f64a0e9)
5. [DTO pattern](https://www.baeldung.com/java-dto-pattern)
6. [Authentication basics (hashing, JWT)](https://medium.com/@nick_92077/user-authentication-basics-hashing-and-jwt-3f9adf12272)
7. [Domain model with SQLAlchemy](https://blog.szymonmiks.pl/p/domain-model-with-sqlalchemy/)

## Practical examples and tutorials

1. [Domain-Driven Design in Practice (Pluralsight)](https://www.pluralsight.com/courses/domain-driven-design-in-practice)
2. [Modular Monolith with DDD](https://github.com/kgrzybek/modular-monolith-with-ddd)
3. [Python DDD implementation](https://github.com/qu3vipon/python-ddd)

## Tools and frameworks

1. [Python dependency injection](https://medium.com/@spraneeth4/python-dependency-injector-simplifying-dependency-injection-in-your-projects-14385af0bf78)
2. [DDD value objects and validation](https://scresh.hashnode.dev/ddd-value-objects-mastering-data-validation-in-python)
3. [FastAPI best practices](https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable)
4. [Unit of Work and repository with SQLModel](https://dev.to/manukanne/a-python-implementation-of-the-unit-of-work-and-repository-design-pattern-using-sqlmodel-3mb5)
5. [Backend logging in FastAPI](https://medium.com/@v0220225/backend-logging-in-python-and-applied-to-fastapi-7b47118d1d92)
6. [GitHub Container Registry](https://computingforgeeks.com/configure-github-container-registry-as-your-docker-registry/)
7. [pytest with Eric](https://pytest-with-eric.com/)
8. [Tactical DDD (Vaadin)](https://vaadin.com/blog/ddd-part-2-tactical-domain-driven-design)
