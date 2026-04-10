# Gestech

An Open Source Commercial Management application focused on streamlining sales operations, customer relationships, and inventory control, providing full visibility over the commercial lifecycle.

## ✨ Core Functionalities

### 1. Customer Management

* Customer registration and profile management
* Contact information and interaction history
* Segmentation and customer classification

### 2. Sales Management

* Quotation and sales order creation
* Pricing, discounts, and promotions
* Sales tracking and history

### 3. Order Processing

* Order validation and status tracking
* Invoicing and billing
* Returns and cancellations handling

### 4. Inventory Management

* Real-time stock tracking
* Product catalog and categorization
* Stock movements (inbound/outbound)

### 5. Supplier & Procurement

* Supplier registration and management
* Purchase orders and supply tracking
* Cost control and restocking

### 6. Financial Overview

* Accounts receivable tracking
* Payment status and reconciliation
* Basic revenue and cash flow visibility

### 7. Reporting & Dashboards

* Sales performance metrics
* Inventory and product insights
* Customer behavior analysis

### 8. User & Access Control

* Role-based permissions
* Secure authentication
* Activity tracking

### 9. Notifications & Alerts

* Low stock alerts
* Order status updates
* Payment reminders

### 10. Integration & Scalability

* API support for external systems
* Modular design for future expansion
* Integration with accounting or ERP systems

## Key Value

* Improves sales efficiency and visibility
* Enhances customer relationship management
* Reduces operational errors through automation
* Supports data-driven commercial decisions

## 🛠️ Tech Stack

### Backend

* **Django**
  High-level Python web framework used to build secure and scalable backend services.
* **Python**
  Core programming language powering the application logic.

### Frontend

* **HTML5 / CSS3**
  Structure and styling of the user interface.
* **JavaScript**
  Client-side interactivity and dynamic behavior.
* **Bootstrap**
  Responsive UI framework for consistent design and layout.

### Data & Persistence

* **PostgreSQL** *(recommended for production)*
Robust relational database.
* **SQLite** *(development)*
Lightweight database for local development.

### Static Assets & UI Libraries

* **Chart.js**
  Data visualization for dashboards and reports.
* **DataTables**
  Advanced table interactions (sorting, filtering, pagination).
* **Font Awesome**
  Icon library for UI enhancement.
* **jQuery**
  DOM manipulation and legacy support for UI components.

### Deployment & Infrastructure

* **Docker**
Containerization platform to ensure consistent environments across development and production.
* **Gunicorn**
WSGI HTTP server used to run the Django application in production.
* **Nginx**
Reverse proxy and web server for handling client requests, serving static files, and load balancing.


## 📂 Project Structure

This project follows a modular Django architecture, where each domain is isolated into its own app to ensure maintainability.

```
Gestech/
├── core/                # Project configuration (settings, urls, wsgi/asgi)
├── customers/           # Customer domain
├── dashboard/           # Admin/dashboard interface
├── members/             # User and authentication domain
├── orders/              # Order management domain
├── stock/               # Inventory management domain
├── static/              # Global static assets
│   ├── css/
│   ├── js/
│   ├── img/
|   └── vendor/          # Frontend Libraries
└── templates/           # Global templates
    └── registration/
```

### Core Layer

* **core/**
  Contains global configuration such as settings, URL routing, and application entry points.

### Domain Apps

Each app encapsulates a specific business domain:

* **customers/** → Customer data and related operations
* **members/** → Authentication and user management
* **orders/** → Order lifecycle and processing
* **stock/** → Inventory and stock control

### Interface Layer

* **dashboard/**
  Provides administrative UI, dashboards, and related frontend assets.

### Shared Resources

* **templates/**
  Global templates shared across multiple apps (e.g., authentication views).

* **static/**
  Centralized static assets (CSS, JavaScript, images) used across the application.

## Design Principles

* **Separation of Concerns**: Each app represents a bounded context.
* **Reusability**: Shared templates and static files are centralized.
* **Scalability**: Modular structure allows independent growth of domains.
* **Maintainability**: Clear boundaries reduce coupling between components.


⚙️ Installation
Comming Soon...

