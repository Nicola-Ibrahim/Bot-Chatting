# C4 Model Diagram Guide

The **C4 Model** is a simple way to visualize software architecture at **different levels of detail**.  
It has **four main diagram types**, each serving a different purpose depending on **who you’re talking to** and **what you want to explain**.

Think of it like zooming in with Google Maps:

1. **Context** = Country view
2. **Container** = City view
3. **Component** = Street view
4. **Code** = Building floor plan

---

## 1. **Context Diagram**

**Goal:** Show how your system fits into the **big picture**.  
**Audience:** Non-technical stakeholders, managers, new team members.

**When to use:**

- Presenting the project to business people or a new team.
- Explaining how your system interacts with other systems and users.

**What it shows:**

- Your **system** (as one big box)
- **External systems** (APIs, services, partners)
- **Users** (roles, actors)
- **Relationships** (data flow, interactions)

**Example:**  
If you’re building an **Online Bookstore**, the context diagram might show:

- The Online Bookstore system
- Users: Customers, Admins
- External systems: Payment Gateway, Shipping Service, Email Service
- Arrows showing “Customer orders book”, “Payment Gateway processes payment”, etc.

---

## 2. **Container Diagram**

**Goal:** Show the **major technology building blocks** inside your system.  
**Audience:** Developers, tech leads, architects.

**When to use:**

- Deciding how to split the system into deployable parts.
- Showing what technologies are used for each part.

**What it shows:**

- **Containers** (apps, services, databases, queues)
- **Technologies** (Node.js, PostgreSQL, Redis, etc.)
- **Communication paths** (REST, gRPC, messaging)

**Example:**  
The Online Bookstore container diagram might show:

- **Web App** (React + Node.js)
- **Mobile App** (React Native)
- **Order Service** (Spring Boot + PostgreSQL)
- **Payment Service** (Python + Stripe API)
- **Message Queue** (RabbitMQ)
- Connections between them.

---

## 3. **Component Diagram**

**Goal:** Show the **internal structure** of one container.  
**Audience:** Developers working on that specific container.

**When to use:**

- Planning or explaining the architecture of a microservice or application.
- Showing how logic is split across components.

**What it shows:**

- **Components** (modules, classes, layers)
- **Responsibilities** of each
- **Interfaces / dependencies**

**Example:**  
Inside the **Order Service**, you might have:

- **OrderController** (handles HTTP requests)
- **OrderService** (business logic)
- **PaymentClient** (calls payment API)
- **OrderRepository** (talks to database)

---

## 4. **Code Diagram**

**Goal:** Show **detailed code-level structure**.  
**Audience:** Developers reading or writing the code.

**When to use:**

- Onboarding someone to a specific module.
- Explaining complex logic or class relationships.

**What it shows:**

- **Classes, methods**
- **Relationships** (inheritance, composition, calls)
- **Algorithms** or sequence flows

**Example:**  
You could show how the `OrderService` class calls `PaymentClient`, which then calls Stripe API, and how exceptions are handled.

---

## Quick Decision Table

| Your Goal                                              | Diagram Type  |
|--------------------------------------------------------|---------------|
| Explain **what** the system does and who uses it       | **Context**   |
| Show **how** the system is split into deployable parts | **Container** |
| Explain **what’s inside** a single service or app      | **Component** |
| Explain **exactly how** code works in detail           | **Code**      |

---

**Tips:**

- Start **high-level** (Context) and only go deeper if needed.
- Don’t clutter diagrams—keep them **clear and readable**.
- Use consistent nami
