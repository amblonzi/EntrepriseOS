# Inphora EntrepriseOS — Full Production Review
**Reviewed:** May 14, 2026  
**Reviewer:** Claude Sonnet 4.6  
**Repo:** https://github.com/amblonzi/EntrepriseOS  
**Stack:** FastAPI + PostgreSQL + Redis · React + Vite + TailwindCSS · Podman Compose

---

## Executive Summary

The project has a solid architectural vision — multi-tenant CRM/ERP for African SMEs with a clean React front-end and async FastAPI back-end. The foundations are well-chosen. However, **only ~10–15% of the planned feature set is implemented**, and there are several **critical security and reliability bugs** that must be fixed before any production deployment. This review covers every file in the repository with severity-graded findings and concrete fix code.

---

## Severity Scale

| Level | Meaning |
|-------|---------|
| 🔴 CRITICAL | Security hole, data loss, or crash — fix before any deployment |
| 🟠 HIGH | Functional gap or bad practice that will cause prod incidents |
| 🟡 MEDIUM | Code quality / maintainability issue |
| 🟢 LOW | Enhancement / polish |

---

## 1. Security Issues

### 🔴 CRITICAL — Hardcoded SECRET_KEY (`backend/app/core/security.py`) - **FIXED**

The `SECRET_KEY` is now mandatory in `config.py` and loaded from environment variables.

**Fix:**
```python
# backend/app/core/config.py — add to Settings class:
SECRET_KEY: str  # No default — will raise on startup if unset

ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
REFRESH_TOKEN_EXPIRE_DAYS: int = 7
```
```python
# backend/app/core/security.py
from app.core.config import settings

ALGORITHM = "HS256"

def create_access_token(subject, expires_delta=None):
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return jwt.encode({"exp": expire, "sub": str(subject)}, settings.SECRET_KEY, algorithm=ALGORITHM)
```
```bash
# .env (never committed)
SECRET_KEY=$(openssl rand -hex 32)
```

---

### 🔴 CRITICAL — HTTP 403 typo causes all auth to fail (`backend/app/api/deps.py`) - **FIXED**

The typo `HTTP_03_FORBIDDEN` has been corrected to `HTTP_403_FORBIDDEN`.

---

### 🔴 CRITICAL — Token stored in `localStorage` is XSS-vulnerable (`frontend/src/store/authStore.ts`) - **FIXED**

`authStore.ts` now uses `httpOnly` cookies managed by the backend. `localStorage` is no longer used for tokens.

---

### 🔴 CRITICAL — No rate limiting on `/login` endpoint - **FIXED**

The `/login` endpoint now has rate limiting using `slowapi`.

---

### 🟠 HIGH — No CORS restriction in production (`backend/app/core/config.py`)

`BACKEND_CORS_ORIGINS` defaults to an empty list, but `allow_origins=["*"]` is used in development docker-compose. No enforcement in code to prevent `*` reaching production.

**Fix:**
```python
# backend/app/main.py — replace the CORS middleware block:
allowed_origins = [str(o) for o in settings.BACKEND_CORS_ORIGINS]
if not allowed_origins:
    if settings.ENVIRONMENT == "production":
        raise RuntimeError("BACKEND_CORS_ORIGINS must be set in production")
    allowed_origins = ["http://localhost:3000"]
```

---

### 🟠 HIGH — Passwords logged via SQLAlchemy `echo=True` (`backend/app/db/session.py`)

```python
# CURRENT
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
```

`echo=True` logs every SQL statement. INSERT statements for users include hashed passwords in the log. Logs are often shipped to external services.

**Fix:**
```python
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=settings.ENVIRONMENT == "development",
    pool_size=10,
    max_overflow=20,
)
```

---

### 🟡 MEDIUM — Seed file ships with default admin credentials

`admin@inphora.com` / `admin123` is hardcoded in `seed.py`. If this ever runs against prod (CI/CD accident, wrong env), it creates a known account.

**Fix:** Read credentials from environment variables:
```python
import os
admin_email = os.environ["SEED_ADMIN_EMAIL"]
admin_password = os.environ["SEED_ADMIN_PASSWORD"]
```

---

## 2. Back-end Functional Gaps

### 🟠 HIGH — No Alembic migrations wired up - **FIXED**

Alembic migrations have been initialized and are used for schema management.

---

### 🟠 HIGH — CRM endpoint missing PATCH/DELETE, no pagination headers

`GET /crm/leads` returns up to 100 leads but sends no `X-Total-Count` header, making client-side pagination impossible.

**Fix — add to `crm.py`:**
```python
from fastapi.responses import JSONResponse

@router.get("/leads")
async def read_leads(db, current_user, skip=0, limit=50):
    total_q = await db.execute(select(func.count(Lead.id)).where(Lead.tenant_id == current_user.tenant_id))
    total = total_q.scalar()
    result = await db.execute(select(Lead).where(...).offset(skip).limit(limit))
    leads = result.scalars().all()
    return JSONResponse(
        content=jsonable_encoder(leads),
        headers={"X-Total-Count": str(total), "X-Page-Size": str(limit)}
    )

@router.patch("/leads/{lead_id}", response_model=LeadOut)
async def update_lead(lead_id: UUID, lead_in: LeadUpdate, db=Depends(get_db), current_user=Depends(...)):
    result = await db.execute(select(Lead).where(Lead.id == lead_id, Lead.tenant_id == current_user.tenant_id))
    lead = result.scalars().first()
    if not lead:
        raise HTTPException(404, "Lead not found")
    for field, value in lead_in.dict(exclude_unset=True).items():
        setattr(lead, field, value)
    await db.commit()
    return lead

@router.delete("/leads/{lead_id}", status_code=204)
async def delete_lead(lead_id: UUID, db=Depends(get_db), current_user=Depends(...)):
    result = await db.execute(select(Lead).where(Lead.id == lead_id, Lead.tenant_id == current_user.tenant_id))
    lead = result.scalars().first()
    if not lead:
        raise HTTPException(404)
    lead.is_deleted = True  # soft delete
    await db.commit()
```

---

### 🟠 HIGH — Missing modules: Finance, Inventory, HR, Analytics have zero backend code

All four modules are "coming soon" in the frontend with no backend routes, models, or schemas. The implementation plan covers them but they are entirely absent.

**Minimum viable Finance module additions needed:**

Models: `Invoice`, `InvoiceItem`, `Expense`, `Account`, `Transaction`  
Routes: `POST /finance/invoices`, `GET /finance/invoices`, `PATCH /finance/invoices/{id}`, `POST /finance/invoices/{id}/send`  
Schemas: `InvoiceCreate`, `InvoiceOut`, `ExpenseCreate`

**Minimum viable Inventory additions:**

Models: `Product`, `Warehouse`, `StockItem`, `StockMovement`  
Routes: `GET/POST /inventory/products`, `GET /inventory/stock`

---

### 🟠 HIGH — No refresh token / token rotation

Access tokens expire in 60 minutes (hardcoded, not from settings). There is no refresh token flow. Users are silently logged out hourly.

**Fix — add refresh token:**
```python
# backend/app/core/security.py
def create_refresh_token(subject) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode({"exp": expire, "sub": str(subject), "type": "refresh"}, settings.SECRET_KEY, algorithm=ALGORITHM)
```
```python
# backend/app/api/v1/endpoints/auth.py
@router.post("/refresh")
async def refresh_token(request: Request, db=Depends(get_db)):
    token = request.cookies.get("refresh_token")
    # validate, issue new access_token cookie
```

---

### 🟡 MEDIUM — `UserOut` schema missing `role` and `is_active` fields

```python
# CURRENT — schemas/auth.py
class UserOut(UserBase):
    id: UUID
    tenant_id: UUID
```

The frontend reads `user.role` to display in the TopBar, but `role` is not included in `UserOut`. This silently returns `undefined`.

**Fix:**
```python
class UserOut(UserBase):
    id: UUID
    tenant_id: UUID
    role: str
    is_active: bool
```

---

### 🟡 MEDIUM — `LeadStatus` enum values are lowercase in model but uppercase in frontend

```python
# model
class LeadStatus(str, enum.Enum):
    NEW = "new"   # value is "new"
```
```typescript
// frontend — statusColors map keys are uppercase
const statusColors = { 'NEW': '...', 'CONTACTED': '...' }
```
When the API returns `"new"`, the color lookup fails silently (no badge color).

**Fix — align to a single casing.** Recommend uppercase in both:
```python
NEW = "NEW"
CONTACTED = "CONTACTED"
```

---

## 3. Front-end Issues

### 🟠 HIGH — CRM "New Lead" button is non-functional

The `+ New Lead` button in `CRM.tsx` has no `onClick` handler. It renders but does nothing.

**Fix — add a modal/drawer with a form:**
```tsx
const [showModal, setShowModal] = useState(false);

// In the modal:
const handleCreate = async (data: LeadCreate) => {
  await api.post('/crm/leads', data);
  fetchLeads(); // refresh list
  setShowModal(false);
};
```

---

### 🟠 HIGH — Dashboard uses hardcoded mock data, not live API data

```tsx
// Dashboard.tsx
const data = [
  { name: 'Jan', sales: 4000, leads: 2400 },
  ...
];
```

All charts and stat cards show static fake numbers regardless of actual business data.

**Fix:**
```tsx
const [stats, setStats] = useState(null);
useEffect(() => {
  api.get('/analytics/dashboard-summary').then(r => setStats(r.data));
}, []);
```

(Requires a new `GET /analytics/dashboard-summary` backend endpoint that aggregates lead counts, revenue, etc.)

---

### 🟠 HIGH — No error boundary or global error handler

Any unhandled promise rejection or render error will crash the entire app with a blank screen. There is no `<ErrorBoundary>` component.

**Fix:**
```tsx
// src/components/ErrorBoundary.tsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  render() {
    if (this.state.hasError) return <ErrorScreen onRetry={() => this.setState({ hasError: false })} />;
    return this.props.children;
  }
}

// src/main.tsx — wrap App:
<ErrorBoundary><App /></ErrorBoundary>
```

---

### 🟡 MEDIUM — Global search bar in `TopBar.tsx` is purely decorative

The search input has no `onChange` handler and performs no search. It will mislead users.

**Fix:** Implement global search with `useDebounce` and a `GET /search?q=` endpoint, or hide it until implemented.

---

### 🟡 MEDIUM — No loading state guard in `ProtectedRoute`

If `checkAuth` is still in-flight and `isLoading=true`, `ProtectedRoute` will redirect to `/login` before the auth check completes, causing a login flash on every page load.

**Fix:**
```tsx
// ProtectedRoute.tsx
export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuthStore();
  if (isLoading) return <FullPageSpinner />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return children;
};
```

---

### 🟢 LOW — Missing `<title>` tag updates per route

All pages show the same browser tab title. Use `react-helmet-async` or Vite's `vite-plugin-html` to set per-route titles.

---

## 4. Infrastructure & DevOps

### 🟠 HIGH — No health check in `podman-compose.yml`

If the database starts slowly, the backend will crash on startup with a connection error. There is no `healthcheck` or `depends_on.condition`.

**Fix:**
```yaml
# podman-compose.yml
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 10

  backend:
    depends_on:
      db:
        condition: service_healthy
```

---

### 🟠 HIGH — No `.env.example` file

The repo has no `.env.example`. New contributors have no idea which environment variables are required. The app silently fails with cryptic errors.

**Fix — create `.env.example`:**
```dotenv
# Required
POSTGRES_USER=postgres
POSTGRES_PASSWORD=change_me_in_production
POSTGRES_DB=entreprise_os
SECRET_KEY=generate_with_openssl_rand_hex_32

# Optional
REDIS_URL=redis://redis:6379/0
BACKEND_CORS_ORIGINS=http://localhost:3000
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ENVIRONMENT=development
```

---

### 🟠 HIGH — No NGINX reverse proxy config for production

The `nginx.conf` in the frontend container only serves the React SPA. There is no top-level NGINX to route `/api/` → backend and `/` → frontend, which means the frontend's `baseURL: '/api/v1'` will not work in production without manual proxy config.

**Fix — add `nginx/nginx.conf` to repo root:**
```nginx
upstream backend {
    server backend:8000;
}

server {
    listen 80;
    
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://frontend:80;
    }
}
```
And add a `nginx` service to `podman-compose.yml`.

---

### 🟡 MEDIUM — No CI/CD pipeline

There are no GitHub Actions workflows despite the implementation plan referencing them. No tests run on PR, no lint checks, no container builds on merge.

**Minimum CI (`/.github/workflows/ci.yml`):**
```yaml
on: [push, pull_request]
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r backend/requirements.txt
      - run: cd backend && python -m pytest tests/
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: cd frontend && npm ci && npm run build
```

---

### 🟢 LOW — Podman Compose vs Docker Compose note

The project uses `podman-compose` but most CI systems and many developers have Docker Compose. Adding a `docker-compose.yml` symlink or alias note in the README lowers friction significantly.

---

## 5. Missing Planned Features (from `implementation_plan.md`)

| Feature | Status | Priority |
|---------|--------|----------|
| RBAC / granular permissions | ❌ Not started — role is a plain string | 🟠 HIGH |
| Finance module (GL, invoicing, expenses) | ❌ Not started | 🟠 HIGH |
| Inventory module (stock, warehouses) | ❌ Not started | 🟠 HIGH |
| HR & Payroll | ❌ Not started | 🟡 MEDIUM |
| Analytics / KPI dashboard | ❌ Hardcoded mock data | 🟠 HIGH |
| Projects / task management | ❌ Not started | 🟡 MEDIUM |
| Celery background tasks | ❌ In requirements, not wired | 🟡 MEDIUM |
| Multi-currency / M-Pesa / eTIMS | ❌ Not started | 🟡 MEDIUM (Africa-specific) |
| MFA | ❌ Not started | 🟡 MEDIUM |
| Refresh token flow | ❌ Not started | 🟠 HIGH |
| Alembic migrations | ❌ `create_all` only | 🟠 HIGH |
| Tests (backend + frontend) | ❌ Not started | 🟠 HIGH |

---

## 6. Recommended Fix Priority Order

**Sprint 0 — Before any real usage (1–2 days):**
1. Fix the `HTTP_03_FORBIDDEN` typo (crashes auth completely)
2. Move `SECRET_KEY` to environment variable
3. Migrate tokens from `localStorage` to `httpOnly` cookies
4. Add rate limiting to `/login`
5. Set `echo=False` in production DB engine
6. Fix `LeadStatus` enum case mismatch

**Sprint 1 — Core reliability (1 week):**
7. Add `role` field to `UserOut` schema
8. Wire up Alembic migrations
9. Implement refresh token flow
10. Add NGINX reverse proxy
11. Add health checks to compose
12. Add `.env.example`
13. Wire up "New Lead" modal with create form
14. Add `ErrorBoundary` component
15. Fix `ProtectedRoute` loading flash

**Sprint 2 — Feature completeness (2–4 weeks):**
16. Finance module (models + API + UI)
17. Inventory module (models + API + UI)
18. Live Dashboard analytics endpoint
19. Full RBAC system
20. CI/CD pipeline (GitHub Actions)

**Sprint 3 — Production hardening:**
21. Tests (pytest for backend, Vitest/Playwright for frontend)
22. Monitoring (Prometheus + Grafana)
23. M-Pesa / eTIMS integration hooks
24. MFA

---

## 7. What's Working Well ✅

- Multi-tenant architecture is correctly designed — `tenant_id` on every row is the right approach
- Async FastAPI with asyncpg is a solid, performant choice
- Zustand for auth state is clean and minimal
- Tailwind + shadcn/ui design system is consistent and looks professional
- Soft-delete pattern (`is_deleted`) on the base model is production-correct
- Podman over Docker is a good security decision for containerisation
- The implementation plan is thoughtful and well-structured

---

*Generated by Claude Sonnet 4.6 · Full source review of commit `main` · May 14, 2026*
