# Technical Specifications

## 1. Introduction

### Purpose
This document provides detailed technical specifications for the software architecture and components of Project Edge.

### Scope
It covers API specifications, data models, system architecture, security, performance, testing, and deployment strategies.

## 2. API Specifications

### Endpoint Definitions

1. **User Management**
   - **Path:** `/api/users`
   - **Methods:** 
     - `POST`: Create a new user.
     - `GET`: Get user profile information.
     - `PUT`: Update user profile information.
     - `DELETE`: Delete user account.
   - **Request Parameters:**
     - `POST`: `first_name` (required), `last_name` (required), `email` (required), `password` (required).
     - `PUT`: `first_name`, `last_name`, `description`, `areas_of_interest`, `email`, `password`.
   - **Response Structures:**
     - `POST`, `GET`, `PUT`: `id`, `first_name`, `last_name`, `description`, `areas_of_interest`, `email`.
   - **Status Codes:**
     - `200 OK`: Successful operation.
     - `400 Bad Request`: Invalid request parameters.
     - `401 Unauthorized`: Authentication failure.
     - `404 Not Found`: User not found.
     - `500 Internal Server Error`: Server error.

2. **Post Management**
   - **Path:** `/api/posts`
   - **Methods:**
     - `POST`: Create a new post.
     - `GET`: Get posts.
     - `PUT`: Update a post.
     - `DELETE`: Delete a post.
   - **Request Parameters:**
     - `POST`: `title` (required), `description` (required), `owners` (optional).
     - `PUT`: `title`, `description`.
   - **Response Structures:**
     - `POST`, `GET`, `PUT`: `id`, `title`, `description`.
   - **Status Codes:**
     - `200 OK`: Successful operation.
     - `400 Bad Request`: Invalid request parameters.
     - `401 Unauthorized`: Authentication failure.
     - `404 Not Found`: Post not found.
     - `500 Internal Server Error`: Server error.

3. **Comment Management**
   - **Path:** `/api/comments`
   - **Methods:**
     - `POST`: Create a new comment.
     - `GET`: Get comments for a specific post.
     - `PUT`: Update a comment.
     - `DELETE`: Delete a comment.
   - **Request Parameters:**
     - `POST`: `description` (required), `post_id` (required), `user_id` (required).
     - `PUT`: `description`, `comment_id` (required).
     - `DELETE`: `comment_id` (required).
   - **Response Structures:**
     - `POST`, `GET`, `PUT`: `id`, `description`, `user_id`, `post_id`.
   - **Status Codes:**
     - `200 OK`: Successful operation.
     - `400 Bad Request`: Invalid request parameters.
     - `401 Unauthorized`: Authentication failure.
     - `404 Not Found`: Comment not found.
     - `500 Internal Server Error`: Server error.

4. **Notification Management**
   - **Path:** `/api/notifications`
   - **Methods:**
     - `GET`: Retrieve notifications.
     - `PUT`: Mark notifications as read.
     - `DELETE`: Clear notifications.
   - **Request Parameters:**
     - `GET`: `user_id` (required).
     - `PUT`: `notification_id` (required).
     - `DELETE`: `notification_id` (optional, clear all if not specified).
   - **Response Structures:**
     - `GET`: List of notifications.
     - `PUT`, `DELETE`: Status message.
   - **Status Codes:**
     - `200 OK`: Successful operation.
     - `400 Bad Request`: Invalid request parameters.
     - `401 Unauthorized`: Authentication failure.
     - `404 Not Found`: Notification not found.
     - `500 Internal Server Error`: Server error.

5. **Message Management**
   - **Path:** `/api/messages`
   - **Methods:**
     - `POST`: Send a message.
     - `GET`: Retrieve messages.
     - `DELETE`: Delete a message.
   - **Request Parameters:**
     - `POST`: `receiver_id` (required), `content` (required).
     - `GET`: `user_id` (required), `sender_id` (optional).
     - `DELETE`: `message_id` (required).
   - **Response Structures:**
     - `POST`, `GET`, `DELETE`: Status message or list of messages.
   - **Status Codes:**
     - `200 OK`: Successful operation.
     - `400 Bad Request`: Invalid request parameters.
     - `401 Unauthorized`: Authentication failure.
     - `404 Not Found`: Message not found.
     - `500 Internal Server Error`: Server error.

6. **Search and Filtering**
   - **Path:** `/api/search`
   - **Methods:**
     - `GET`: Search posts.
   - **Request Parameters:**
     - `GET`: `query` (required), `tags` (optional), `categories` (optional), `type` (optional).
   - **Response Structures:**
     - `GET`: List of matched posts/discussions.
   - **Status Codes:**
     - `200 OK`: Successful operation.
     - `400 Bad Request`: Invalid request parameters.
     - `500 Internal Server Error`: Server error.

### Authentication Mechanisms
- **JWT Authentication:** Users must include an Authorization header with a valid JWT token in requests.

### Error Handling
- **Standard API Error Responses:**
  - **Format:** JSON
  - **Structure:**
    ```json
    {
      "error": {
        "code": "<error_code>",
        "message": "<error_message>"
      }
    }
    ```
- **Status Codes and Messages:**
  - `400 Bad Request`: Invalid request parameters.
  - `401 Unauthorized`: Authentication required.
  - `403 Forbidden`: Access denied.
  - `404 Not Found`: Resource not found.
  - `500 Internal Server Error`: Internal server error.
 
### 3. Data Models

- **User:**
  - `id`: Integer (Primary Key)
  - `first_name`: String (50 characters, not nullable)
  - `last_name`: String (50 characters, not nullable)
  - `email`: String (100 characters, unique, not nullable)
  - `password`: String (255 characters, not nullable)
  - `description`: String (1000 characters, nullable)
  - `tag_ids`: Integer[] (Foreign Key to `Tag.id`, nullable)

- **Post:**
  - `id`: Integer (Primary Key)
  - `title`: String (255 characters, not nullable)
  - `description`: String (1000 characters, not nullable)
  - `user_id`: Integer (Foreign Key to `User.id`, not nullable)
  - `tag_ids`: Integer[] (Foreign Key to `Tag.id`, nullable)

- **ProjectPost:**
  - Inherits from `Post`
  - `members`: Integer[] (Foreign Key to `User.id`, nullable)

- **Tag:**
  - `id`: Integer (Primary Key)
  - `descriptor`: String (50 characters, unique, not nullable)

- **Comment:**
  - `id`: Integer (Primary Key)
  - `description`: String (1000 characters, not nullable)
  - `user_id`: Integer (Foreign Key to `User.id`, not nullable)
  - `post_id`: Integer (Foreign Key to `Post.id`, not nullable)

- **Notification:**
  - `id`: Integer (Primary Key)
  - `user_id`: Integer (Foreign Key to `User.id`, not nullable)
  - `content`: String (255 characters, not nullable)
  - `timestamp`: DateTime (nullable, default: current timestamp)

- **Message:**
  - `id`: Integer (Primary Key)
  - `sender_id`: Integer (Foreign Key to `User.id`, not nullable)
  - `receiver_id`: Integer (Foreign Key to `User.id`, not nullable)
  - `content`: String (1000 characters, not nullable)
  - `timestamp`: DateTime (nullable, default: current timestamp)

- **Reaction:**
  - `id`: Integer (Primary Key)
  - `user_id`: Integer (Foreign Key to `User.id`, not nullable)
  - `post_id`: Integer (Foreign Key to `Post.id`, nullable)
  - `comment_id`: Integer (Foreign Key to `Comment.id`, nullable)
  - `reaction_type`: Enum ('LIKE', 'DISLIKE', not nullable)
  - `timestamp`: DateTime (nullable, default: current timestamp)

- **Attachment:**
  - `id`: Integer (Primary Key)
  - `post_id`: Integer (Foreign Key to `Post.id`, nullable)
  - `comment_id`: Integer (Foreign Key to `Comment.id`, nullable)
  - `file_url`: String (255 characters, not nullable)
  - `file_type`: String (50 characters, not nullable)
  - `timestamp`: DateTime (nullable, default: current timestamp)

### 4. Entity Relationships

Provide an entity-relationship diagram to visually demonstrate the database schema and how the entities connect.

### 5. Data Flow Diagrams

Include diagrams that illustrate the flow of data through different actions:

1. **User Registration/Login:**
```plaintext
User -> API Gateway -> User Service -> Database
```

2. **Post Creation:**
```plaintext
User -> API Gateway -> Post Service -> Database
```

3. **Adding Comments:**
```plaintext
User -> API Gateway -> Comment Service -> Database
```

### 6. Service Architecture

#### Microservices Layout

1. **User Service**
   - **Responsibilities:** Manages user authentication, profiles, and roles.
   - **Interactions:** Communicates with Post Service and Notification Service for user activities.

2. **Post Service**
   - **Responsibilities:** Handles CRUD operations for posts and related data.
   - **Interactions:** Collaborates with User Service for validating user actions.

3. **Notification Service**
   - **Responsibilities:** Manages notifications for users.
   - **Interactions:** Subscribes to events from User and Post Services to generate notifications.

4. **Message Service**
   - **Responsibilities:** Manages direct messaging between users.
   - **Interactions:** Works with User Service for authentication and user data.

5. **Attachment Service**
   - **Responsibilities:** Manages file attachments for posts and comments.
   - **Interactions:** Utilizes storage services for file management.

#### Internal APIs

1. **User Service API**
   - **Endpoints:** `/api/users`
   - **Purpose:** Handles user management and authentication.

2. **Post Service API**
   - **Endpoints:** `/api/posts`
   - **Purpose:** Manages posts and discussions.

3. **Notification Service API**
   - **Endpoints:** `/api/notifications`
   - **Purpose:** Manages notifications for user activities.

4. **Message Service API**
   - **Endpoints:** `/api/messages`
   - **Purpose:** Handles sending and receiving messages between users.

5. **Attachment Service API**
   - **Endpoints:** `/api/attachments`
   - **Purpose:** Manages file uploads and retrievals.

#### External Integrations

1. **Email Service**
   - **Purpose:** Integrates with external email providers for sending notifications and verifications.

2. **Storage Service**
   - **Purpose:** Integrates with cloud storage platforms for file attachments.

3. **Analytics Service**
   - **Purpose:** Integrates with analytics platforms to track user engagements and behaviors.

### 7. Security Specifications

#### Data Security

- **Encryption:** All sensitive data stored in the database is encrypted using industry-standard algorithms.
- **Access Control:** Role-based access control to restrict data access.
- **Secure Communication:** All client-server communications are secured using HTTPS.
- **Regular Security Audits:** Conduct regular security audits to identify vulnerabilities.

#### Compliance and Standards

- **GDPR:** Protecting user data and privacy in the European Union.
- **HIPAA:** Ensuring the security and privacy of health-related information.

#### Vulnerability Management

- **Patch Management:** Regularly apply security patches.
- **Vulnerability Scanning:** Conduct regular scans to identify potential security weaknesses.
- **Incident Response Plan:** Maintain a plan for responding to and mitigating security incidents.

### 8. Performance and Scaling

#### Performance Benchmarks

- **Response Time:** Aim for an average API response time under 500 milliseconds.
- **Throughput:** Handle a minimum of 1000 concurrent users without performance degradation.

#### Scaling Strategy

- **Horizontal Scaling:** Add more server instances to handle increased load.
- **Load Balancing:** Distribute incoming traffic evenly across servers.
- **Database Sharding:** Partition database to manage large data sets efficiently.

### 9. Testing Strategy

#### Testing Levels

1. **Unit Testing:** Validate individual components.
2. **Integration Testing:** Ensure components work together correctly.
3. **System Testing:** Validate the entire system meets requirements.
4. **Acceptance Testing:** Ensure the platform meets users' expectations.

#### Test Cases

- **User Registration:** Verify new user account creation.
- **Post Creation:** Ensure posts can be created with correct attributes.
- **Authentication:** Validate secure login and access to authorized resources.

#### Automation Strategy

- **Automated Tests:** Use frameworks to automate test cases.
- **Continuous Integration:** Integrate automated tests into CI/CD to detect issues early.

### 10. Deployment Strategy

#### Environment Setup

- **Development:** Local setups using Docker Compose.
- **Testing:** Dedicated environments for running automated tests.
- **Staging:** Pre-production environments for final validation.
- **Production:** Hosted on cloud platforms like AWS, Azure, or Google Cloud for scalability and reliability.

#### Deployment Process

- **Code Review:** Peer review for quality assurance.
- **Automated Builds:** Trigger builds automatically upon code commits.
- **Continuous Deployment:** Use tools like GitHub Actions or Jenkins for deployment automation.

#### Rollback Procedures

- **Automated Rollback:** Scripts to revert to the last stable version.
- **Rollback Testing:** Test rollback in staging environments before production.
- **Incident Response:** Protocols for prompt communication and resolution.

### 11. Maintenance and Monitoring

#### Monitoring Tools

- **Prometheus:** Collects and monitors metric data.
- **Grafana:** Visualizes and analyzes resource utilization.
- **ELK Stack:** Centralizes logging for log analysis and troubleshooting.

#### Log Management

- **Log Storage:** Centralized infrastructure for logs.
- **Log Rotation:** Policies for managing log file sizes.
- **Log Analysis:** Tools to parse and analyze logs for identifying issues.

#### Maintenance Procedures

- **Database Backups:** Schedule regular backups to ensure data recovery.
- **Software Updates:** Apply patches to address vulnerabilities.
- **Performance Tuning:** Continuously monitor and optimize system performance.

### 12. Conclusion

#### Summary

This document outlines the technical specifications and strategies for developing, deploying, and maintaining Project Edge, a community-driven platform for university students.
