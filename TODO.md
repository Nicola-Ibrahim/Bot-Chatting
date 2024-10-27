# TODO List for Version 2.0

### Core Functionalities

1. **User Authentication**:
   - [ ] Implement login and registration endpoints
   - [ ] Set up JWT authentication
   - [ ] Secure sensitive routes with authentication middleware
   - [ ] Write unit and integration tests for authentication

2. **User Dashboard**:
   - [ ] Create a user dashboard with basic profile information
   - [ ] Add settings page for changing password and preferences

3. **Notifications System**:
   - [ ] Set up a notification service for user events (email and in-app notifications)
   - [ ] Create a notification UI component
   - [ ] Integrate notifications with key user actions (e.g., new registrations, password resets)

4. **Observer Pattern for Email Notifications and Logging**:
   - [ ] **Implement the Observer pattern** to decouple notification logic from the core business logic.
     - Use **FastAPI** for the implementation.
     - Observers will be responsible for:
       - Sending email notifications on specific events (e.g., user registration, password change).
       - Writing to the logging system when these events are triggered.
   - [ ] Write unit tests to ensure proper observer behavior for:
     - Successful email sending.
     - Logging entries on specific user actions.

---

### Implementation Details

- **Sending Email Notifications**:
  - Observer class that listens for specific events like new user registration or password resets.
  - Upon receiving an event, the observer will handle the logic for sending email notifications.
  - Use an SMTP server or an email service like SendGrid, depending on the configuration.

- **Logging System**:
  - Implement another observer that writes logs (e.g., successful email sent, failed attempts) to a logging system when an event is triggered.
  - Use the `logging` library for logging, with appropriate log levels (e.g., `INFO`, `ERROR`).

### Proposed Class Structure

- **EventPublisher**: This class will allow subscribers (observers) to register and notify them when events happen.
- **EmailObserver**: Observes user-related events and handles sending emails.
- **LoggingObserver**: Observes the same events and writes logs to the logging system.

```python
# Example of Observer Pattern in FastAPI
from typing import List
import logging

# Base classes for Observer Pattern
class EventPublisher:
    def __init__(self):
        self._observers: List = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def notify_observers(self, event_data):
        for observer in self._observers:
            observer.update(event_data)


class Observer:
    def update(self, event_data):
        raise NotImplementedError


# Concrete Observers
class EmailObserver(Observer):
    def update(self, event_data):
        # Implement email sending logic
        print(f"Sending email for event: {event_data}")
        # Here, you would use FastAPI's Background Tasks or other async email-sending functionality


class LoggingObserver(Observer):
    def update(self, event_data):
        logging.info(f"Logging event: {event_data}")


# Usage within FastAPI
from fastapi import FastAPI

app = FastAPI()

# Create instances of observers
email_observer = EmailObserver()
logging_observer = LoggingObserver()

# Create a publisher and register observers
event_publisher = EventPublisher()
event_publisher.register_observer(email_observer)
event_publisher.register_observer(logging_observer)

@app.post("/user/register")
async def register_user(user_data: dict):
    # User registration logic (e.g., save to the database)
    
    # Notify observers about the event
    event_publisher.notify_observers(f"User {user_data['email']} registered")
    
    return {"message": "User registered successfully"}

```

### Additional Considerations

Ensure that the email sending process is done asynchronously, using FastAPI’s BackgroundTasks or another async approach to avoid blocking the main thread.
Add comprehensive error handling for both email sending and logging actions

### Explanation

- **EventPublisher**: Manages a list of observers and notifies them of events.
- **EmailObserver**: Handles the logic for sending emails when notified.
- **LoggingObserver**: Logs the event data when notified.
- The **notify_observers** method is called after an event (like user registration), triggering the observers to perform their tasks.

You can further customize the logic and implement the observer pattern as per your requirements, ensuring that emails and logs are handled asynchronously where necessary.
