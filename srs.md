# Software Requirements Specification (SRS)
## Saimazoom – Distributed Order Management System

---

## 1. Introduction

Saimazoom is a distributed system designed to manage online product orders through coordinated interaction between multiple actors. The system is structured around a centralized controller that manages state transitions and task assignments via message queues.

### 1.1 Purpose

The purpose of this document is to define the functional requirements and system architecture of Saimazoom.

### 1.2 Actors

- **Client** – Places and manages product orders.
- **Central Controller** – Coordinates system workflow and maintains system state.
- **Robot** – Retrieves products from warehouse storage.
- **Delivery Agent** – Delivers products to the client.
- **Administrator** – Manages database and system configuration.

---

## 2. System Description

Saimazoom operates as a coordinated distributed system.

### 2.1 Operational Flow

1. A Client submits an order request.
2. The Controller registers the order and assigns a Robot.
3. The Robot transports the product to the conveyor system.
4. The Controller assigns a Delivery Agent.
5. The product is delivered to the Client.

All communication between actors is handled via message queues.

---

## 3. Functional Requirements

### 3.1 Client Logic

- **CL1** – Client registration with unique identifier.
- **CL2** – Order creation specifying product ID.
- **CL3** – Retrieve list of orders with status information.
- **CL4** – Cancel an existing order.

### 3.2 Controller Logic

- **CT1** – Register new orders.
- **CT2** – Maintain order status lifecycle.
- **CT3** – Assign tasks to Robots.
- **CT4** – Assign tasks to Delivery Agents.
- **CT5** – Ensure system state consistency.

---

## 4. Architectural Considerations

- Centralized coordination model
- Asynchronous communication through message queues
- State-based order lifecycle management
- Role-based system separation

---

## 5. Conclusion

This specification defines the structural and functional foundation of a distributed order management system. The design emphasizes modular role separation and coordinated communication via message queues.
