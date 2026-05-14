# Inphora EntrepriseOS - Project Walkthrough

Inphora EntrepriseOS is now initialized with a modern, production-grade architecture. This document explains how the system is structured and how to get started.

## 1. Project Structure

- **`backend/`**: FastAPI application.
  - `app/models/`: SQLAlchemy models with UUIDs and soft deletes.
  - `app/api/`: Versioned API endpoints (v1).
  - `app/core/`: Security (JWT, Hashing) and Configuration.
  - `Containerfile`: Podman build instructions.
- **`frontend/`**: React + Vite application.
  - `src/components/layout/`: Modern Sidebar, TopBar, and DashboardLayout.
  - `src/features/dashboard/`: Executive overview with Recharts.
  - `src/lib/utils.ts`: Tailwind utility for shadcn/ui.
  - `Containerfile`: Multi-stage build (Node -> Nginx).
- **`podman-compose.yml`**: Orchestrates the entire stack (PostgreSQL, Redis, Backend, Frontend).

## 2. How to Run

### Prerequisites
- Podman and Podman Compose installed.

### Steps
1. **Start the containers**:
   ```bash
   podman-compose up --build
   ```
2. **Initialize the Database**:
   Run the seeding script (within the backend container):
   ```bash
   podman exec -it entreprise-backend python seed.py
   ```
3. **Access the Platform**:
   - Frontend: `http://localhost:3000`
   - API Docs: `http://localhost:8000/docs`

## 3. Current Features

- **Multi-tenancy**: Data is logically isolated by `tenant_id`.
- **Modern UI**: Dark/Light mode ready, mobile-responsive, elegant charts.
- **Authentication**: Secure JWT login with role support.
- **CRM Foundation**: Lead management model and API endpoints.

## 4. Next Steps

1. **Implement Finance Module**: General Ledger and Invoicing models.
2. **Inventory Management**: Product catalog and warehouse tracking.
3. **M-Pesa Integration**: Integration-ready structure for payments.
4. **RBAC Refinement**: Granular permissions in the database.
