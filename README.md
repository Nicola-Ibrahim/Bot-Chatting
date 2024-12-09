# 🤖 **Bot Chat System**

## 🚀 **Overview**

This repository contains a bot system built using **FastAPI** and applying **Domain-Driven Design (DDD)** principles. The system is designed to integrate core features like **authentication**, **user management**, and **bot conversations**, while maintaining modularity, scalability, and maintainability. Each feature is encapsulated in its own bounded context, following DDD best practices for separation of concerns.

### 🌟 **Key Features**

- **FastAPI**: A high-performance web framework used to build the API, providing asynchronous support and automatic API documentation via Swagger.
- **Domain-Driven Design (DDD)**: The architecture follows DDD principles, ensuring that business logic and components like user management and authentication are isolated and clearly defined.
- **Authentication & Authorization**: The system supports secure login via JWT tokens, enforcing role-based access control for users.
- **Bot Conversations**: The bot engages in interactive conversations, handling user inputs, generating responses, and maintaining conversation states.
- **Notifications**: The system sends notifications about key events, such as message updates or system alerts, keeping users informed in real-time.

```bash
Bot-Chat/
├── src/
│   ├── chat/                                  # Bounded Context: Chat - Handles user interactions, messages, and chat-based logic
│   │   ├── application/
│   │   │   ├── interfaces/                     # Interfaces for chat services
│   │   │   └── services/                       # Chat-related services (e.g., response handling)
│   │   ├── domain/
│   │   │   ├── entities/                       # Chat entities (e.g., message, conversation)
│   │   │   ├── value_objects/                  # Value objects related to chat (e.g., message status)
│   │   │   └── exceptions/                     # Exceptions related to chat processes
│   │   ├── presentation/
│   │   │   ├── contract/                       # Interfaces for chat API contracts
│   │   │   └── web/                            # Web layer for chat (e.g., API routes)
│   │   ├── infra/
│   │   │   ├── repository/                     # Chat repository for storing data (e.g., messages, conversations)
│   │   │   └── utils/                          # Utility functions for chat (e.g., message formatting)
│
│   ├── ai/                                    # Bounded Context: AI - Handles AI-related logic, like models for responses
│   │   ├── application/
│   │   │   ├── interfaces/                     # AI service interfaces
│   │   │   └── services/                       # AI-related services (e.g., model inference)
│   │   ├── domain/
│   │   │   ├── entities/                       # AI-related entities
│   │   │   ├── value_objects/                  # Value objects for AI, like model configuration
│   │   │   └── exceptions/                     # AI-specific exceptions
│   │   ├── presentation/
│   │   │   ├── contract/                       # AI service contracts (e.g., input/output format)
│   │   │   └── web/                            # AI web layer for API interaction
│   │   ├── infra/
│   │   │   ├── repository/                     # AI-related repository for storing models or configurations
│   │   │   └── utils/                          # Utility functions for AI tasks (e.g., data preprocessing)
│
│   ├── accounts/                              # Bounded Context: Accounts - Handles user registration, authentication, and profiles
│   │   ├── application/
│   │   │   ├── interfaces/                     # Interfaces for user-related services
│   │   │   └── services/                       # User-related services (e.g., authentication, user management)
│   │   ├── domain/
│   │   │   ├── entities/                       # User entities (e.g., user, role)
│   │   │   ├── value_objects/                  # Value objects for user (e.g., email, password)
│   │   │   └── exceptions/                     # Exceptions related to user operations
│   │   ├── presentation/
│   │   │   ├── contract/                       # Contracts for user services (e.g., user creation API)
│   │   │   └── web/                            # User API routes (e.g., login, registration)
│   │   ├── infra/
│   │   │   ├── repository/                     # User repository for DB interactions
│   │   │   └── utils/                          # User-related utilities (e.g., password hashing)
│
│   ├── notification/                          # Bounded Context: Notifications - Handles system notifications to users
│   │   ├── application/
│   │   │   ├── interfaces/                     # Notification service interfaces
│   │   │   └── services/                       # Notification services (e.g., email, SMS)
│   │   ├── domain/
│   │   │   ├── entities/                       # Notification-related entities
│   │   │   ├── value_objects/                  # Value objects for notifications (e.g., notification types)
│   │   │   └── exceptions/                     # Notification-specific exceptions
│   │   ├── presentation/
│   │   │   ├── contract/                       # Contracts for notification services
│   │   │   └── web/                            # Notification API routes (e.g., send email, SMS)
│   │   ├── infra/
│   │   │   ├── repository/                     # Repository for storing notification records
│   │   │   └── utils/                          # Notification utilities (e.g., template rendering)
│
│   ├── access_control/                       # Bounded Context: Access Control - Handles authentication and authorization
│   │   ├── application/
│   │   │   ├── interfaces/                     # Access control service interfaces (e.g., permissions)
│   │   │   └── services/                       # Access control services (e.g., user role management)
│   │   ├── domain/
│   │   │   ├── entities/                       # Entities related to roles and permissions
│   │   │   ├── value_objects/                  # Value objects related to access control (e.g., role name)
│   │   │   └── exceptions/                     # Access control-related exceptions
│   │   ├── presentation/
│   │   │   ├── contract/                       # Contracts for access control (e.g., role management API)
│   │   │   └── web/                            # Access control API routes (e.g., login, permissions)
│   │   ├── infra/
│   │   │   ├── repository/                     # Repository for access control data (e.g., roles, permissions)
│   │   │   └── utils/                          # Access control utilities (e.g., JWT token generation)
│
│   ├── shared/                                # Shared Modules - Common services, schemas, and utilities across contexts
│   │   ├── services/                           # Shared business logic and common services
│   │   ├── schemas/                            # Pydantic schemas for validation across contexts
│   │   └── utils/                              # Utility functions used across multiple contexts
│   │   ├── presentation/
│   │   │   ├── api/                          # FastAPI app resides here for API layer across all contexts
│   │   │   └── cli/                          # CLI app resides here for command-line interface across contexts
│
│   ├── infrastructure/                        # Infrastructure Layer - Common infrastructure services
│   │   ├── config/                            # Configuration setup for all services (e.g., DB URL, API keys)
│   │   ├── security/                          # Security utilities (e.g., JWT handling, encryption)
│   │   ├── logging_config/                    # Centralized logging setup for all services
│   │   ├── repository/                        # Generic repository for interactions with data models
│   │   └── utils/                             # Generic utilities used across infrastructure
│
├── .env                                       # Environment variables (e.g., database URLs, secrets)
├── pyproject.toml                             # Dependency management for the project
├── Dockerfile                                 # Docker configuration for containerization
├── pre_commit_config.yaml                     # Pre-commit hooks configuration for code quality
├── README.md                                  # Documentation for the microservice
└── .gitignore                                 # Git ignore settings for unnecessary files
```

# Bot System Documentation

🚀 **Bot System** powered by **FastAPI** and **DDD**  
The bot system follows Domain-Driven Design (DDD) principles, facilitating a clean and manageable architecture. It integrates key features like **authentication**, **conversations**, **notifications**, and more, using FastAPI for building high-performance APIs.

---

## 🛠️ **Core Layer: Domain Logic**

The **Core Layer** handles the main business logic, domain models, and services. Each **bounded context** in the system, such as **chat**, and **auth** has its own domain-driven services and entities.

---

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

#### **Schema**

- **auth_schema.py**: Defines validation schemas for authentication, including fields for username, password, and JWT tokens.

---

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

#### **Schema**

- **conversation_schema.py**: Defines the structure of a conversation, including messages and sender information.

---

## 📣 **Notifications**

The system can send notifications to users about new messages, order statuses, or other relevant events.

#### **Endpoints**

- **POST /notifications/email**: Send an email notification to a user.

  - **Request Body:**

    ```json
    {
      "to": "user@example.com",
      "subject": "Order Status",
      "body": "Your order has been shipped."
    }
    ```

- **POST /notifications/sms**: Send an SMS notification to a user.

  - **Request Body:**

    ```json
    {
      "to": "+1234567890",
      "message": "Your order has been shipped."
    }
    ```

#### **Schema**

- **notification_schema.py**: Defines the structure for notification details (e.g., email, SMS).

---

## 🛡️ **Configuration and Security**

The system’s configuration is stored in environment variables, such as the database URL and the JWT secret. Security mechanisms include **password hashing** and **JWT** token generation and validation.

#### **Key Files**

- **config.py**: Configuration settings (e.g., JWT secret, database URL).
- **security.py**: Contains utilities for securing passwords and handling JWT tokens.

---

## 🧪 **Testing**

To ensure all features are functional, the bot system includes unit and integration tests.

#### **Test Endpoints**

- **POST /test/authentication**: Test user authentication.
- **POST /test/orders**: Test order creation functionality.

#### **Test Files**

- **test_auth.py**: Unit tests for authentication logic.
- **test_orders.py**: Unit tests for order-related functionality.

---

## 📄 **Running the Application**

1. **Set Up Environment:**  
   Create a `.env` file with the necessary environment variables, including `DATABASE_URL`, `JWT_SECRET_KEY`, etc.

2. **Install Dependencies:**  
   Run `pip install -r requirements.txt` to install all dependencies.

3. **Start the Server:**  
   Run the FastAPI server with:

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access API Docs:**  

    Once the server is running, you can access the interactive API documentation through Swagger UI at:  
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
    This provides a user-friendly interface to explore and test all available API endpoints directly.

## 🔧 **Conclusion**  

By following **Domain-Driven Design** and utilizing **FastAPI**, this bot system is highly modular and easily extendable. With clear boundaries between different concerns (such as authentication, notifications, and conversations), it’s easy for new developers to contribute and expand the system. The detailed documentation and organized file structure will guide you through the system, making it simple to understand and interact with the project.

## Useful Resources

For further reading and strengthening DDD skills:

- [ ] [Domain-Driven Design](https://herbertograca.com/2017/09/07/domain-driven-design/)
- [ ] [Onion Architecture](https://medium.com/expedia-group-tech/onion-architecture-deed8a554423)
- [ ] [implementing-dddomain-models](https://medium.com/vx-company/implementing-dddomain-models-ports-adapters-and-cqrs-with-c-2b81403f09f7)
- [ ] [implementing-ports-CQRS](https://abstarreveld.medium.com/dddomain-models-ports-adapters-and-cqrs-reference-architecture-c-504817df65ec)
- [ ] [clean-lessonsUse cases](https://medium.com/unil-ci-software-engineering/clean-ddd-lessons-use-cases-e9d11f64a0e9)
- [ ] [Clean Domain-Driven Design](https://medium.com/unil-ci-software-engineering/clean-domain-driven-design-2236f5430a05)
- [ ] [Always-Valid Domain Model](https://vkhorikov.medium.com/always-valid-domain-model-706e5f3d24b0)
- [ ] [DDD Value Objects: Mastering Data Validation in Python](https://scresh.hashnode.dev/ddd-value-objects-mastering-data-validation-in-python)
- [ ] [Domain-Driven Design (DDD) and Hexagonal Architecture in Java](https://vaadin.com/blog/ddd-part-3-domain-driven-design-and-the-hexagonal-architecture)
- [ ] [DTO pattern (Data Transfer Object)](https://www.baeldung.com/java-dto-pattern)
- [ ] [Domain model with SQLAlchemy](https://blog.szymonmiks.pl/p/domain-model-with-sqlalchemy/)
