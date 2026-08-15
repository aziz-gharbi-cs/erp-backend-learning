# ERP Backend — Backlog

## 🔐 Authentication & Security

- [ ] Test missing JWT → `401 Unauthorized`
- [ ] Test invalid JWT → `401 Unauthorized`
- [ ] Test wrong password → `401 Unauthorized`
- [ ] Test inactive user → `401 Unauthorized`
- [ ] Implement role-based authorization
- [ ] Create `require_role()` dependency
- [ ] Create `require_admin()` dependency
- [ ] Test insufficient permissions → `403 Forbidden`
- [ ] Review JWT expiration handling
- [ ] Review invalid/expired token handling
- [ ] Consider refresh-token strategy
- [ ] Review authentication error handling

---

## 👤 Users & Employees

- [ ] Finish User ↔ Employee relationship
- [ ] Create `UserService`
- [ ] Create `user_schema.py`
- [ ] Implement user retrieval
- [ ] Implement user update
- [ ] Implement user deletion/deactivation
- [ ] Implement user activation/deactivation
- [ ] Implement password change
- [ ] Decide which fields belong to `User`
- [ ] Decide which fields belong to `Employee`
- [ ] Review User/Employee responsibilities

---

## 🧱 FastAPI Architecture

- [x] FastAPI application
- [x] API routing
- [x] Dependency injection
- [x] Database session dependency
- [x] Authentication dependency
- [x] `/auth/register`
- [x] `/auth/login`
- [x] `/auth/me`
- [ ] Protect business endpoints with `get_current_user`
- [ ] Apply role-based authorization to protected endpoints
- [ ] Review HTTP status codes
- [ ] Standardize API error handling
- [ ] Review service/repository boundaries
- [ ] Keep business logic out of repositories

---

## 🗄️ Database & Alembic

- [x] SQLAlchemy models
- [x] PostgreSQL connection
- [x] Alembic configuration
- [x] Initial migration
- [x] Customer phone migration
- [x] Employee authentication migration
- [x] Users migration
- [x] `alembic upgrade head`
- [x] `alembic check`
- [ ] Review latest migration
- [ ] Keep migrations synchronized with models
- [ ] Verify downgrade paths
- [ ] Establish migration workflow

### Migration Workflow

Whenever a model changes:

```text
Modify Model
     ↓
alembic revision --autogenerate -m "description"
     ↓
Review migration manually
     ↓
alembic upgrade head
     ↓
alembic check
     ↓
Commit migration + model