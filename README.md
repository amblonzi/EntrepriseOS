# Inphora EntrepriseOS

A production-grade modern web-based CRM + ERP platform for SMEs and growing enterprises in Africa.

## Core Modules
- **CRM**: Lead & Contact management, Sales pipeline.
- **Finance**: General ledger, Invoicing, Expenses.
- **Inventory**: Stock management, Multi-warehouse support.
- **HR & Payroll**: Employee management, Payslips.
- **Analytics**: Executive dashboards and real-time KPIs.

## Tech Stack
- **Frontend**: React.js, Vite, TailwindCSS, shadcn/ui, Framer Motion.
- **Backend**: FastAPI (Python), Async architecture, JWT Auth, RBAC.
- **Database**: PostgreSQL & Redis.
- **Infrastructure**: Podman & Podman Compose.

## Getting Started

### Prerequisites
- Podman installed and running.
- Python 3.10+ (for podman-compose module).

### Running Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/amblonzi/EntrepriseOS.git
   cd EntrepriseOS
   ```
2. Start the services:
   ```bash
   python -m podman_compose up --build
   ```
3. Initialize the database:
   ```bash
   podman exec -it entreprise-backend python seed.py
   ```

### URLs
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000/docs`

## License
MIT
