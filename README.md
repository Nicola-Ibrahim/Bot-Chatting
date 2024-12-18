# 🤖 **Bot Chat System**

## 🚀 **Overview**

This repository contains a **Bot Chat System** built with **FastAPI** and adhering to **Domain-Driven Design (DDD)** principles. The system is modular, scalable, and maintainable, integrating essential features such as **authentication**, **user management**, and **bot conversations**.

The architecture is designed using **Clean Architecture** and **Modularization of a Monolithic Application**, ensuring that each feature operates within its own **bounded context**. This separation of concerns helps in managing complexity and promoting long-term maintainability.

### 🌟 **Key Features**

- **FastAPI**: High-performance web framework for building APIs, offering asynchronous support and automatic API documentation via Swagger.
- **Domain-Driven Design (DDD)**: The system follows DDD principles to maintain clear boundaries and isolate business logic in dedicated modules.
- **Authentication & Authorization**: Secure login using JWT tokens with role-based access control (RBAC).
- **Bot Conversations**: The bot interacts with users, processes input, and manages conversation states.
- **Notifications**: Real-time notifications are sent about key events, such as message updates or system alerts, ensuring users stay informed.

## 🔍 **System Overview**

This bot system is designed with modularity in mind, following best practices to ensure the system is both scalable and maintainable. The implementation leverages **Clean Architecture** principles and **Modularization of the Monolith** to provide a clear separation of concerns between different modules.

Key components include:

- **Core Layer**: Houses the main domain logic, including business rules, entities, and value objects.
- **Application Layer**: Contains use cases that orchestrate interactions between domain services and external interfaces like APIs.
- **Infrastructure Layer**: Manages communication with external resources, such as databases, message queues, and external APIs.
- **Presentation Layer**: Exposes the FastAPI API for external consumers, providing endpoints for interaction with the system.

Each feature (e.g., **auth**, **chat**, **notifications**) is encapsulated within its own bounded context, making the system easy to extend and maintain.

## 🛠️ **Core Layer: Domain Logic**

The **Core Layer** is the heart of the system, responsible for the main business logic and domain models. In this layer, we define:

- **Entities**: Business objects that have a distinct identity (e.g., `User`, `Participants`).
- **Value Objects**: Immutable objects that represent concepts in the domain (e.g., `Content`, `Feedback`).
- **Aggregates**: Collections of entities and value objects treated as a unit (e.g., `Conversation`. `Message`).
- **Domain Services**: Provide business logic that doesn't naturally belong to an entity (e.g., `UserService`, `MessageService`).

This layered architecture ensures clear boundaries between business logic, infrastructure concerns, and application-specific code.

## 📄 **Running the Application**

For more details on setting up and running the application, please refer to the [Running the Application guide](./BUILDING.md).

### 🧑‍💻 **Authentication & Authorization**

The system uses **JWT** for secure user authentication. Upon successful login, a token is issued, which must be provided in subsequent requests to validate user actions.

#### **Endpoints**

- **POST /auth/login**: User login endpoint to authenticate and return a JWT token.

  - **Request Body:**

    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```

  - **Response:**

    ```json
    {
      "access_token": "jwt_token",
      "token_type": "bearer"
    }
    ```

- **POST /auth/refresh**: Refresh JWT token.

  - **Request Body:**

    ```json
    {
      "refresh_token": "string"
    }
    ```

  - **Response:**

    ```json
    {
      "access_token": "new_jwt_token"
    }
    ```

## 💬 **Bot Conversations**

The **Conversation** entity manages the bot interactions with users, maintaining the conversation flow and ensuring state consistency.

#### **Endpoints**

- **GET /conversations/{conversation_id}**: Fetch a specific conversation by its ID.

  - **Response:**

    ```json
    {
      "conversation_id": "string",
      "messages": [
        {
          "sender": "bot",
          "content": "Hello, how can I assist you?"
        }
      ]
    }
    ```

- **POST /conversations/{conversation_id}/messages**: Send a message to the conversation.

  - **Request Body:**

    ```json
    {
      "sender": "user",
      "content": "I need help with my order"
    }
    ```

  - **Response:**

    ```json
    {
      "message_id": "string",
      "status": "sent"
    }
    ```

## 🔧 **Conclusion**

By following **Domain-Driven Design** and utilizing **FastAPI**, this bot system is highly modular and easily extendable. With clear boundaries between different concerns (such as authentication, notifications, and conversations), it’s easy for new developers to contribute and expand the system. The detailed documentation and organized file structure will guide you through the system, making it simple to understand and interact with the project.

# 📚 Useful Resources for Domain-Driven Design (DDD)

## 🏗️ Core Concepts and Architectures

1. **Herberto Graca Blog**: [Domain-Driven Design](https://herbertograca.com/2017/09/07/domain-driven-design/)
   An in-depth exploration of DDD principles and their practical applications.

2. **Medium**: [Onion Architecture](https://medium.com/expedia-group-tech/onion-architecture-deed8a554423)
   An article discussing the Onion Architecture and its relation to DDD.

3. **GitHub**: [Modular Monolith with DDD](https://github.com/kgrzybek/modular-monolith-with-ddd)
   A repository demonstrating how to build a modular monolith using DDD principles.

4. **Medium**: [Clean Domain-Driven Design](https://medium.com/unil-ci-software-engineering/clean-domain-driven-design-2236f5430a05)
   Insights into maintaining clean architecture while implementing DDD.

5. **Medium**: [Always-Valid Domain Model](https://vkhorikov.medium.com/always-valid-domain-model-706e5f3d24b0)
   Emphasizing the importance of maintaining validity within domain models.

6. **GitHub**: [Clean Architecture by Examples](https://github.com/amantinband/clean-architecture)
   A collection of examples illustrating clean architecture practices.

7. **GitHub**: [Python DDD Implementation](https://github.com/qu3vipon/python-ddd)
   A repository showcasing Domain-Driven Design implemented in Python.

8. **Pluralsight (*tutorial*)**: [Domain-Driven Design in Practice](https://www.pluralsight.com/courses/domain-driven-design-in-practice)
   A comprehensive course offering practical insights into DDD.

9. **Code Maze**: [Clean Architecture with .NET](https://code-maze.com/dotnet-clean-architecture/)
   A guide to implementing clean architecture principles in .NET applications.

10. **Vaadin Blog**: [Domain-Driven Design (DDD) and Hexagonal Architecture in Java](https://vaadin.com/blog/ddd-part-3-domain-driven-design-and-the-hexagonal-architecture)
    Exploring the integration of DDD with Hexagonal Architecture in Java applications.

## ⚙️ Implementation Patterns

1. **Medium**: [Implementing DDD Domain Models](https://medium.com/vx-company/implementing-dddomain-models-ports-adapters-and-cqrs-with-c-2b81403f09f7)
   A discussion on implementing domain models using Ports, Adapters, and CQRS.

2. **Medium**: [Implementing Ports & CQRS](https://abstarreveld.medium.com/dddomain-models-ports-adapters-and-cqrs-reference-architecture-c-504817df65ec)
   A reference architecture for DDD models, ports, adapters, and CQRS.

3. **Baeldung**: [DTO Pattern (Data Transfer Object)](https://www.baeldung.com/java-dto-pattern)
   An explanation of the DTO pattern and its usage in Java applications.

4. **Medium**: [Clean Lessons: Use Cases](https://medium.com/unil-ci-software-engineering/clean-ddd-lessons-use-cases-e9d11f64a0e9)
   Insights into designing use cases within clean architecture frameworks.

## 🛠️ Tools and Frameworks

1. **Blog**: [Domain Model with SQLAlchemy](https://blog.szymonmiks.pl/p/domain-model-with-sqlalchemy/)
   A guide on implementing domain models using SQLAlchemy in Python.

2. **Hashnode**: [DDD Value Objects: Mastering Data Validation in Python](https://scresh.hashnode.dev/ddd-value-objects-mastering-data-validation-in-python)
   Focusing on data validation within DDD value objects in Python.

3. **GitHub**: [FastAPI Best Practices: Project Structure](https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable)
   Best practices for structuring FastAPI projects, relevant to DDD implementations.

4. **Dev.to**: [Unit of Work and Repository Design Patterns with SQLModel](https://dev.to/manukanne/a-python-implementation-of-the-unit-of-work-and-repository-design-pattern-using-sqlmodel-3mb5)
   A Python implementation of the Unit of Work and Repository design patterns using SQLModel.

5. **Medium**: [Backend Logging in Python with FastAPI](https://medium.com/@v0220225/backend-logging-in-python-and-applied-to-fastapi-7b47118d1d92)
   A guide on implementing backend logging in Python applications using FastAPI.

6. **ComputingForGeeks**: [Configure GitHub Container Registry as Your Docker Registry](https://computingforgeeks.com/configure-github-container-registry-as-your-docker-registry/)
   Instructions on setting up GitHub Container Registry for Docker images.
