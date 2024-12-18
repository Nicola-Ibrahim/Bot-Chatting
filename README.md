# 🤖 **Bot Chat System**

## 🚀 **Overview**

This repository contains a bot system built using **FastAPI** and applying **Domain-Driven Design (DDD)** principles. The system is designed to integrate core features like **authentication**, **user management**, and **bot conversations**, while maintaining modularity, scalability, and maintainability. Each feature is encapsulated in its own bounded context, following DDD best practices for separation of concerns.

### 🌟 **Key Features**

- **FastAPI**: A high-performance web framework used to build the API, providing asynchronous support and automatic API documentation via Swagger.
- **Domain-Driven Design (DDD)**: The architecture follows DDD principles, ensuring that business logic and components like user management and authentication are isolated and clearly defined.
- **Authentication & Authorization**: The system supports secure login via JWT tokens, enforcing role-based access control for users.
- **Bot Conversations**: The bot engages in interactive conversations, handling user inputs, generating responses, and maintaining conversation states.
- **Notifications**: The system sends notifications about key events, such as message updates or system alerts, keeping users informed in real-time.

# Bot System Documentation

🚀 **Bot System** powered by **FastAPI** and **DDD**  
The bot system follows Domain-Driven Design (DDD) principles, facilitating a clean and manageable architecture. It integrates key features like **authentication**, **conversations**, **notifications**, and more, using FastAPI for building high-performance APIs.

## 🛠️ **Core Layer: Domain Logic**

The **Core Layer** handles the main business logic, domain models, and services. Each **bounded context** in the system, such as **chat**, and **auth** has its own domain-driven services and entities.

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
