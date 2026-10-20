# NEXUS ERP — AI-Powered Enterprise Resource Planning

**Building the next generation of enterprise software through backend engineering, intelligent automation, and applied AI.**

NEXUS ERP is an extensible Enterprise Resource Planning platform designed to unify business operations through a modular backend architecture and an AI-powered intelligence layer. The project combines modern Python backend technologies with a vision for intelligent business analytics, predictive insights, and controlled AI-driven workflows.

The goal is to explore how reliable enterprise software can integrate with modern AI systems while maintaining security, data integrity, scalability, and human oversight.

## ✨ Key Features

- **Modular Backend Architecture** — Layered application design separating API endpoints, business logic, data access, validation, and persistence.
- **Enterprise Data Management** — A foundation for managing products, customers, employees, suppliers, inventory, and financial operations.
- **Database Engineering** — Relational data modeling with PostgreSQL, SQLAlchemy ORM, and version-controlled migrations using Alembic.
- **AI Business Copilot** — Planned integration of Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and structured tool calling for business intelligence.
- **Intelligent Automation** — Planned AI-assisted workflows for inventory optimization, procurement, document processing, and operational decision support.
- **Security by Design** — Authentication, role-based access control, input validation, auditability, and controlled execution of sensitive operations.
- **Cloud-Native Engineering** — A roadmap covering containerization, asynchronous processing, CI/CD, monitoring, and deployment automation.

## 🧠 AI Architecture Vision

NEXUS ERP aims to go beyond traditional dashboards by introducing an AI Business Operations Copilot.

The proposed architecture combines three complementary layers:

1. **Business Data Layer:** Structured enterprise data stored in PostgreSQL and accessed through validated application services.
2. **AI Intelligence Layer:** LLMs, RAG, semantic search, and machine learning for contextual question answering, forecasting, and anomaly detection.
3. **Workflow Execution Layer:** Controlled AI tool calling, business-rule validation, permission checks, human approvals, and auditable actions.

The AI system is intended to retrieve evidence from enterprise data, explain its recommendations, and assist with operational decisions without bypassing application security or business rules.

## 🏗️ Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Backend | FastAPI, Uvicorn |
| Validation | Pydantic |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL |
| Migrations | Alembic |
| Caching | Redis |
| AI & LLMs | LLM APIs, RAG, tool calling |
| Agent orchestration | LangGraph — planned |
| Vector search | pgvector — planned |
| Testing | pytest, HTTPX |
| Infrastructure | Docker, Docker Compose — planned |
| CI/CD | GitHub Actions — planned |
| Observability | Prometheus, Grafana, OpenTelemetry — planned |

*Technologies marked as planned represent the target architecture, not necessarily implemented functionality.*

## 🏛️ Architecture

The backend follows a layered architecture designed to separate responsibilities and make the application easier to test, maintain, and extend.

```text
                 Client / API Consumer
                         |
                         v
                  FastAPI Routers
                         |
                         v
                  Pydantic Schemas
                         |
                         v
                    Service Layer
                         |
                         v
                  Repository Layer
                         |
                         v
                  SQLAlchemy ORM
                         |
                         v
                     PostgreSQL

        Future AI Integration
        ├── LLM Integration
        ├── RAG and Semantic Search
        ├── AI Business Copilot
        └── Controlled Agentic Workflows
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/aziz-gharbi-cs/erp-backend-learning.git
cd erp-backend-learning
```

### 2. Create a virtual environment

**Linux / WSL**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file using the variable names expected by your application configuration. For example:

```dotenv
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/nexus_erp
```

Create the PostgreSQL database and configure your actual credentials. Never commit secrets or production credentials to GitHub.

### 5. Apply database migrations

If Alembic is configured in the project:

```bash
alembic upgrade head
```

### 6. Start the API

```bash
uvicorn app.main:app --reload
```

Adjust `app.main:app` if your application entry point differs.

Once the server is running, open the interactive API documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 🧪 Testing

Run the automated tests with:

```bash
pytest
```

The project aims to cover API behavior, data validation, business logic, database interactions, authentication, and critical workflow edge cases.

## 🗺️ Roadmap

- [ ] Complete core ERP entities and business workflows.
- [ ] Strengthen authentication, authorization, and automated test coverage.
- [ ] Add inventory and procurement business rules.
- [ ] Integrate an AI copilot with authorized, read-only business tools.
- [ ] Implement document ingestion, RAG, and source-grounded answers.
- [ ] Add controlled AI-assisted actions with human approval.
- [ ] Explore predictive analytics and demand forecasting.
- [ ] Containerize the application and automate CI/CD.
- [ ] Introduce structured logging, metrics, tracing, and performance testing.

## 🔒 Engineering Principles

NEXUS ERP is guided by a few core principles:

- **Security first:** Authentication and authorization must be enforced by trusted application code.
- **Data integrity:** Financial and inventory operations require validated business rules and consistent transactions.
- **AI with guardrails:** AI-generated recommendations must be validated before consequential actions are executed.
- **Testability:** Critical behavior should be verifiable through automated tests.
- **Maintainability:** Clear module boundaries and explicit dependencies should make the system easier to evolve.
- **Incremental engineering:** New technologies should solve concrete problems rather than add unnecessary complexity.

## 🎯 Project Objective

NEXUS ERP is an evolving engineering project focused on the intersection of enterprise backend development, applied AI, and cloud-native systems. Its long-term ambition is to demonstrate how intelligent automation can be integrated into business software without compromising reliability, security, or human control.

**Built to learn, engineered to scale, designed for intelligent business operations.**

## 👨‍💻 Author

**Ahmed Aziz Gharbi**

Computer Science Engineering Student | Backend Engineering | Applied AI | Systems & DevOps

[GitHub](https://github.com/aziz-gharbi-cs)

---

*Project status: Under development. Consult the repository for the currently implemented features and supported configuration.*
