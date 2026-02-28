# Saimazoom – Distributed Order Management System Design

System design and requirements specification for a distributed order management platform based on message-queue communication between multiple actors.

## Overview

Saimazoom is a conceptual distributed system designed to manage online orders through coordinated interaction between different roles:

- **Client** – Places and manages product orders.
- **Central Controller** – Coordinates the full order lifecycle.
- **Robots** – Retrieve products from the warehouse.
- **Delivery Agents** – Deliver products to customers.
- **Administrator** – Manages the controller database and system configuration.

All communications between actors are handled through a message queue architecture.

## System Architecture

The system follows a centralized coordination model:

1. A **Client** places an order.
2. The **Controller** assigns the product retrieval task to a **Robot**.
3. Once the product is placed on the conveyor system, the **Controller** assigns delivery to a **Delivery Agent**.
4. The product is delivered to the **Client**.

The controller maintains state management for:
- Clients
- Orders
- Products
- Robots
- Delivery agents

## Functional Requirements

### Client Logic
- User registration with unique identifier
- Order creation
- Order status retrieval
- Order cancellation

### Controller Logic
- Order registration and status tracking
- Task assignment to robots
- Task assignment to delivery agents
- State consistency management

## Technical Concepts Applied

- Distributed system modeling
- Message queue communication
- Role-based system architecture
- Functional requirement specification (SRS)
- State lifecycle design
- System interaction flow definition

## Documentation

Full Software Requirements Specification available in:

`srs_p2.md`

## Purpose

This project demonstrates system modeling skills and structured specification of distributed architectures before implementation.
