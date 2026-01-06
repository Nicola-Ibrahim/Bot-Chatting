# 🔐 Authentication and RBAC

The Horizon Chat System implements a secure, token-based authentication system with fine-grained **Role-Based Access Control (RBAC)**.

---

## 🛡️ Security Principles

- **Stateless Auth**: We use **JWT (JSON Web Tokens)** for stateless authentication.
- **Password Hashing**: Passwords are never stored in plain text; we use industry-standard hashing (e.g., Argon2 or BCrypt via Passlib).
- **Separation of Concerns**: Authentication logic is encapsulated within the `accounts` module.

---

## 🎭 Role-Based Access Control (RBAC)

We support multiple roles to control access to different parts of the system:
- **Admin**: Full access to user management and system settings.
- **User**: Standard access to create and participate in conversations.
- **Bot**: Limited access specifically for AI-driven interactions.

Permissions are checked both at the **API layer** (FastAPI dependencies) and the **Domain layer** (Business Rules).

---

## 📡 API Endpoints

### Login
`POST /auth/login`
**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```
**Response**:
```json
{
  "access_token": "ey...",
  "refresh_token": "ey...",
  "token_type": "bearer"
}
```

### Token Refresh
`POST /auth/refresh`
Exchange a refresh token for a new access token without re-authenticating.

---

> [!IMPORTANT]
> Always ensure that your `JWT_SECRET_KEY` is kept secure and never committed to version control. Use a `.env` file for local development.
