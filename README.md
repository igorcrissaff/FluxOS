# Gestech
Open-Source Comercial Management Software

## 🚀 Overview
Basic Overview

## ✨ Functions
Summary of functions

## 🛠️ Tech Stack
List of tools used

## 📂 Project Structure

## Directory Layout
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

