# Inphora EntrepriseOS - Implementation Plan

Inphora EntrepriseOS is a modern, production-grade CRM + ERP platform designed specifically for SMEs and growing enterprises in Africa. It unifies essential business operations into a single, scalable SaaS-ready system.

## 1. System Architecture

The system follows a **Modular Monolith** architecture transitioning towards microservices. It uses a **Multi-tenant** design with data isolation.

### High-Level Components
- **Frontend**: SPA built with React + Vite, communicating with the backend via REST and WebSockets.
- **API Layer**: FastAPI handles requests, authentication, and orchestrates services.
- **Worker Layer**: Celery handles background tasks (emails, PDF generation, reorder calculations).
- **Cache Layer**: Redis for session storage, rate limiting, and task queue.
- **Data Layer**: PostgreSQL as the primary relational database with UUID-based IDs and soft deletes.

### Multi-tenancy Strategy
We will use the **Column-based Isolation** approach:
- Every table includes a `tenant_id` (UUID).
- Application-level middleware ensures all queries are filtered by the current user's `tenant_id`.
- This approach simplifies multi-branch and multi-company support within a single organization.

## 2. Folder Structure

```text
inphora-entreprise-os/
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── core/           # Config, Security, Auth, Utils
│   │   ├── db/             # Base, Session, Migrations
│   │   ├── models/         # SQLAlchemy Models (Unified)
│   │   ├── schemas/        # Pydantic Schemas
│   │   ├── modules/        # Domain-driven modules
│   │   │   ├── crm/        # Leads, Contacts, Pipeline
│   │   │   ├── finance/    # Ledger, Invoicing, Expenses
│   │   │   ├── inventory/  # Stock, Warehouses, Suppliers
│   │   │   └── hr/         # Employees, Payroll, Leave
│   │   ├── services/       # Business logic (Service Layer)
│   │   ├── api/            # API Route definitions
│   │   └── main.py         # Entry point
│   ├── tests/
│   ├── alembic/            # Migrations
│   ├── requirements.txt
│   └── Containerfile
├── frontend/               # React + Vite Application
│   ├── src/
│   │   ├── assets/
│   │   ├── components/     # UI components (shadcn/ui)
│   │   ├── features/       # Modular features (crm, finance, etc.)
│   │   ├── hooks/          # Custom React hooks
│   │   ├── lib/            # Utils, Axios config
│   │   ├── store/          # Zustand state management
│   │   ├── types/          # TypeScript definitions
│   │   └── App.tsx
│   ├── tailwind.config.js
│   └── Containerfile
├── podman-compose.yml
├── nginx/                  # NGINX configuration
└── .env.example
```

## 3. Database Schema Design (Core)

### Global Tables
- `tenants`: `id, name, domain, plan_id, created_at`
- `users`: `id, tenant_id, email, hashed_password, role_id, is_active`
- `roles`: `id, name, permissions (JSONB)`

### CRM Module
- `leads`: `id, tenant_id, name, email, status, source, assigned_to`
- `contacts`: `id, tenant_id, company_id, name, phone, email`
- `opportunities`: `id, tenant_id, lead_id, value, stage, probability`

### Inventory Module
- `products`: `id, tenant_id, name, sku, category_id, base_price`
- `warehouses`: `id, tenant_id, name, location`
- `stock_items`: `id, tenant_id, product_id, warehouse_id, quantity`

### Finance Module
- `accounts`: `id, tenant_id, name, type (Asset/Liability/Equity), balance`
- `invoices`: `id, tenant_id, customer_id, total, status, due_date`
- `transactions`: `id, tenant_id, account_id, amount, type (Debit/Credit)`

## 4. Authentication & RBAC

- **Auth**: JWT based (Access + Refresh tokens).
- **RBAC**: Granular permissions stored in JSONB in the `roles` table.
- **Middleware**: Custom dependency in FastAPI to check `user.role.permissions` for each endpoint.

## 5. Development Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] Infrastructure setup (Podman, CI/CD).
- [ ] Core Auth & User Management.
- [ ] Tenant provisioning system.
- [ ] Basic UI Layout & Design System.

### Phase 2: CRM & Finance Core (Weeks 3-5)
- [ ] Lead & Contact management.
- [ ] Invoicing and Basic Ledger.
- [ ] Expense tracking.

### Phase 3: Inventory & Supply Chain (Weeks 6-8)
- [ ] Product Catalog & Multi-warehouse stock.
- [ ] Purchase orders & Supplier management.

### Phase 4: HR & Automation (Weeks 9-11)
- [ ] Employee management & Attendance.
- [ ] Workflow engine for approvals.

### Phase 5: Analytics & Polish (Weeks 12+)
- [ ] Executive dashboards (Recharts).
- [ ] Multi-currency and Localization (eTIMS/M-Pesa).
- [ ] Advanced Security (MFA).

## 6. Deployment Strategy
- **Cloud**: AWS/Hetzner with Podman or K8s.
- **CI/CD**: GitHub Actions for automated testing and deployment.
- **Monitoring**: Prometheus + Grafana.
