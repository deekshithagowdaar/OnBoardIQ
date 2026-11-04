# OnboardIQ – Agentic AI-Powered Employee Onboarding Orchestrator

[![Dayforce AI Innovation Challenge](https://img.shields.io/badge/Challenge-Dayforce%20AI%20Innovation-blue.svg)](https://dayforce.com)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB.svg)](https://reactjs.org)
[![LangGraph](https://img.shields.io/badge/Agent%20Orchestration-LangGraph-FF6F00.svg)](https://langchain.com)
[![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178C6.svg)](https://www.typescriptlang.org)
[![Python](https://img.shields.io/badge/Language-Python%203.11%2B-3776AB.svg)](https://python.org)
[![Tests](https://img.shields.io/badge/Tests-12%20Passed-brightgreen.svg)]()

> **Dayforce AI Innovation Challenge Project**  
> OnboardIQ transforms employee onboarding from a passive checklist tracker into an active recovery and workflow optimization engine. It coordinates cross-departmental dependencies, detects upstream delay propagation, quantifies downstream blast radii, simulates recovery strategies in isolated ephemeral sandboxes, and executes manager-approved self-healing workflows.

---

## Table of Contents
1. [Problem Statement & Proposed Solution](#1-problem-statement--proposed-solution)
2. [Key Innovations](#2-key-innovations)
3. [End-to-End System Workflow](#3-end-to-end-system-workflow)
4. [Technology Stack](#4-technology-stack)
5. [System Architecture](#5-system-architecture)
6. [Folder Structure](#6-folder-structure)
7. [Database Design Overview](#7-database-design-overview)
8. [AI Agent Responsibilities (LangGraph)](#8-ai-agent-responsibilities-langgraph)
9. [REST API Overview](#9-rest-api-overview)
10. [Installation & Setup Instructions](#10-installation--setup-instructions)
11. [How to Run Tests](#11-how-to-run-tests)
12. [Main End-to-End Demonstration Walkthrough](#12-main-end-to-end-demonstration-walkthrough)
13. [Mock Integrations & Limitations](#13-mock-integrations--limitations)

---

## 1. Problem Statement & Proposed Solution

### The Problem
Employee onboarding requires intricate coordination across multiple corporate departments: **HR, IT, Payroll, and Benefits**. 

Existing HRIS and onboarding systems provide static checklists and task assignments. However, when complex dependencies arise, simple task tracking fails:
- An employee's **Identity Verification** gets delayed in HR due to a missing passport re-scan.
- As a consequence, **IT System Account Creation** cannot proceed.
- Downstream **Developer Environment Setup** gets blocked.
- The new hire arrives on Day 1 unable to contribute, while cross-functional teams scramble.

Conventional systems merely show that tasks are "pending" without diagnosing why, which downstream tasks are paralyzed, or how to recover.

### The Solution – OnboardIQ
OnboardIQ is an intelligent onboarding recovery and optimization system that:
1. Understands *why* a task is delayed by tracing upstream dependencies to the root cause.
2. Quantifies the downstream *blast radius* on Day-1 technical readiness.
3. Simulates alternative recovery interventions in an isolated in-memory sandbox.
4. Uses a multi-criteria **Recovery Optimizer** to recommend the optimal strategy respecting compliance constraints.
5. Obtains manager approval via a Human-in-the-Loop checkpoint.
6. Automatically executes approved self-healing actions through simulated department APIs, dynamically unblocking the workflow.
7. Learns continuously from historical outcomes to refine future risk models.

---

## 2. Key Innovations

1. **Ephemeral What-If Simulation Sandbox**:
   Unlike systems that force trial-and-error changes on live records, OnboardIQ clones the task graph in memory to evaluate hypothetical actions (e.g. Expedited HR Review vs. Level-2 IT Admin Reassignment vs. Parallel Non-Blocking Reordering) with zero database side-effects until approved.

2. **Constraint-Aware Recovery Optimizer**:
   Ranks scenarios using a multi-criteria utility formulation:
   $$\text{Utility} = (0.35 \times \text{TimeSaved}) + (0.30 \times \text{TasksUnblocked}) + (0.20 \times \text{ReadinessScore}) + (0.15 \times \text{Feasibility})$$
   Enforces compliance guardrails (e.g., mandatory security checks can never be skipped).

3. **Deterministic Graph + LLM Hybrid**:
   Graph traversals, cycle detection, and blast-radius calculations are performed strictly by deterministic math engines (never hallucinated by an LLM), while configurable LLMs synthesize natural language root-cause explanations.

4. **Transparent, Explainable Day-1 Readiness Score (0-100)**:
   Derived from 35% task completion ratio, 25% critical path health, 20% department completion balance, and 20% blocker deductions.

5. **Human-in-the-Loop Safeguards & Audit Ledger**:
   Role-based checkpoints (Manager / HR Admin) ensure sensitive actions require explicit authorization, backed by an immutable audit log.

---

## 3. End-to-End System Workflow

```
New Employee Profile
        ↓
AI-Based Personalized Onboarding Plan
        ↓
Multi-Agent Department Coordination (HR, IT, Payroll, Benefits)
        ↓
Dynamic Dependency Graph & Real-Time Monitoring
        ↓
Predictive Delay & Risk Detection
        ↓
AI Root-Cause & Downstream Blast Radius Analysis
        ↓
Onboarding What-If Simulation & Recovery Optimization
        ↓
Constraint-Aware Self-Healing Workflow
        ↓
Manager Approval for Critical Actions
        ↓
Automated Action Execution & Workflow Adaptation
        ↓
Dynamic Onboarding Readiness Score Recalculation
        ↓
Continuous Learning from Onboarding Outcomes
```

---

## 4. Technology Stack

- **Frontend**:
  - React 18, TypeScript, Vite, Tailwind CSS
  - `@xyflow/react` (React Flow) for interactive Directed Acyclic Graph (DAG) visualization
  - `recharts` for bottleneck analytics and prediction accuracy charts
  - `lucide-react` for enterprise SaaS iconography
  - `axios` for typed REST communication
- **Backend**:
  - Python 3.11+ / 3.14 compatible, FastAPI, Uvicorn
  - Pydantic V2 schemas & validation
  - SQLAlchemy 2.0 ORM
- **Agent Orchestration**:
  - `LangGraph` StateGraph coordinating multi-agent state across HR, IT, Payroll, and Benefits
- **Database**:
  - PostgreSQL (production dockerized) with transparent SQLite fallback for immediate zero-setup execution
- **LLM Integration**:
  - Open-source / local model support via Ollama (`llama3`), with a deterministic high-fidelity fallback mode ensuring 100% functionality without requiring external API keys.

---

## 5. System Architecture

Detailed architecture documentation is available at [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

```
+-------------------------------------------------------------------------+
|                        React 18 Frontend                                |
|  - Main Dashboard (KPIs, Active Blockers, Department Bars)              |
|  - Employee Directory (Search, Department/Status Filters)               |
|  - Onboarding Workspace (Personalized Role Plans, Task Details)         |
|  - Dependency Graph (Interactive React Flow DAG)                        |
|  - Risk & Root-Cause (0-100 Risk Scoring, Blast Radius Diagnostics)     |
|  - What-If Simulator (Ephemeral Sandbox, Scenario A/B/C Comparisons)    |
|  - Recovery & Approvals (Manager Authorization, Self-Healing Execution) |
|  - Readiness Dashboard (Day-1 Gauge, 4-Factor Explainable Formula)      |
|  - Learning & Analytics (Bottleneck Ledger, Prediction MAE)             |
+------------------------------------+------------------------------------+
                                     | REST API (JSON)
                                     v
+-------------------------------------------------------------------------+
|                        FastAPI Backend Engine                           |
|  - Dependency Engine: Cycle detection, upstream/downstream DAG traversal |
|  - Risk Engine: Explainable delay probability and risk score calculation|
|  - Root Cause Engine: Bottleneck diagnosis and blast radius calculation |
|  - Simulation Engine: Ephemeral cloned graph sandbox                    |
|  - Recovery Optimizer: Multi-criteria utility ranking                   |
|  - Readiness Engine: 4-factor mathematical Day-1 readiness scoring      |
|  - LangGraph Orchestrator: Stateful agent workflow                      |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                        Persistence Layer                                |
|  - PostgreSQL / SQLite with 14 Relational Models                        |
|  - Mock Department Gateways (Dayforce HR, IT, Payroll, Benefits)        |
+-------------------------------------------------------------------------+
```

---

## 6. Folder Structure

```
OnboardIQ/
├── backend/
│   ├── app/
│   │   ├── api/             # REST Routers (Employees, Tasks, Graph, Risk, Simulation, Approvals, Readiness, Learning, Agents, Mock)
│   │   ├── engine/          # Deterministic engines (Dependency, Risk, Root Cause, Simulation, Recovery Optimizer, Readiness)
│   │   ├── orchestration/   # LangGraph state graph and department agents
│   │   ├── models/          # SQLAlchemy relational models
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── services/        # Business logic services
│   │   ├── integrations/    # Mock department gateways
│   │   ├── analytics/       # Continuous learning engine
│   │   ├── config.py        # Settings and environment configuration
│   │   ├── database.py      # SQLAlchemy engine and session provider
│   │   ├── seed_data.py     # Database initializer and synthetic demo seeder
│   │   └── main.py          # FastAPI application entry point
│   ├── tests/               # 12 Pytest test cases
│   ├── Dockerfile
│   ├── pytest.ini
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/             # Axios API client
│   │   ├── components/      # Layout, Navbar, Sidebar, CustomTaskNode, StatCard, Badges, Modals
│   │   ├── pages/           # 9 Complete Application Pages
│   │   ├── types/           # TypeScript interfaces
│   │   ├── App.tsx          # Router configuration
│   │   ├── main.tsx         # React root
│   │   └── index.css        # Tailwind and React Flow styling
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── docs/
│   ├── ARCHITECTURE.md      # Detailed system architecture
│   ├── SLIDES_OUTLINE.md    # 5-slide pitch outline
│   └── DEMO_SCRIPT.md       # 10-minute presentation demo script
├── scripts/
│   ├── seed_db.py           # Standalone database seeder
│   ├── start_backend.bat    # Windows backend runner
│   ├── start_backend.sh     # Unix backend runner
│   ├── start_frontend.bat   # Windows frontend runner
│   └── start_frontend.sh    # Unix frontend runner
├── docker-compose.yml       # Multi-container Docker deployment
├── .env.example             # Template environment variables
├── .gitignore
└── README.md
```

---

## 7. Database Design Overview

The database contains 14 relational tables with constraints and indexes:
1. `employees`: Core candidate profiles, roles, locations, equipment, and compliance requirements.
2. `departments`: Organizational departments and department heads.
3. `users`: System users with roles (`HR_ADMIN`, `MANAGER`, `DEPARTMENT_USER`).
4. `onboarding_plans`: Personalized onboarding trajectories.
5. `tasks`: Individual tasks with priority, duration, dates, and status.
6. `task_dependencies`: Directed edges forming the onboarding DAG.
7. `risk_predictions`: Calculated risk scores, categories, and explainable factors.
8. `root_cause_analyses`: Diagnosed root bottlenecks and downstream blast radii.
9. `simulation_scenarios`: Ephemeral simulation records and evaluations.
10. `recovery_recommendations`: Optimal recovery rankings and justifications.
11. `approval_requests`: Authorization queue for critical interventions.
12. `action_executions`: Record of executed self-healing mutations.
13. `readiness_snapshots`: Historical readiness snapshots.
14. `historical_outcomes`: Training ledger for continuous learning and bottleneck analytics.

---

## 8. AI Agent Responsibilities (LangGraph)

Coordinated via a compiled LangGraph `StateGraph`:
- **HR Agent**: Audits identity verification, I-9 compliance forms, employee NDAs, and flags non-compliance.
- **IT Agent**: Monitors system credential provisioning, SSO email generation, laptop logistics, and developer sandbox environments.
- **Payroll Agent**: Verifies direct deposit void checks, tax withholding (W-4) schedules, and payroll registry synchronization.
- **Benefits Agent**: Tracks health, dental, vision, and 401(k) election windows.

---

## 9. REST API Overview

Interactive Swagger documentation is available at `http://localhost:8000/docs`.

| Endpoint | Method | Description |
|---|---|---|
| `/api/employees` | `GET` | List employees with search, department, and status filters |
| `/api/employees` | `POST` | Create a new candidate profile and auto-generate plan |
| `/api/employees/{id}/generate-plan` | `POST` | Regenerate AI-personalized plan |
| `/api/tasks/employee/{id}` | `GET` | Retrieve tasks with attached upstream & downstream dependencies |
| `/api/tasks/{id}` | `PUT` | Update task status and auto-recalculate graph dependencies |
| `/api/tasks/dependencies` | `POST` | Add dependency edge with cycle-detection validation |
| `/api/dependency/{id}/graph` | `GET` | Retrieve React Flow formatted nodes and animated edges |
| `/api/risk/{id}` | `GET` | Run predictive risk engine and return explainable factors |
| `/api/root-cause/{id}` | `GET` | Identify root upstream blocker and downstream blast radius |
| `/api/simulation/{id}/scenarios` | `GET` | Run Scenarios A, B, C side-by-side in ephemeral sandbox |
| `/api/approvals` | `GET` | Retrieve pending and past manager approval requests |
| `/api/approvals/{id}/decide` | `POST` | Approve or reject action; triggers automated execution if approved |
| `/api/readiness/{id}` | `GET` | Calculate 4-factor Day-1 readiness score and critical path checklist |
| `/api/learning/analytics` | `GET` | Retrieve bottleneck analytics, prediction MAE, and strategy success rates |
| `/api/orchestration/run/{id}` | `POST` | Trigger LangGraph multi-agent coordination pipeline |
| `/api/mock/*` | `POST` | Mock Dayforce HR, IT, Payroll, and Benefits gateways |

---

## 10. Installation & Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- (Optional) Docker & Docker Compose for containerized PostgreSQL

---

### Option A: Local Development Setup (Quickest)

#### 1. Start the Backend
```bash
cd OnboardIQ/backend

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Unix/Mac:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server (auto-seeds database on startup)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The backend API is now live at `http://localhost:8000`. OpenAPI docs at `http://localhost:8000/docs`.

#### 2. Start the Frontend
In a new terminal:
```bash
cd OnboardIQ/frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
Open `http://localhost:5173` in your browser.

---

### Option B: Docker Compose Setup

```bash
cd OnboardIQ
docker-compose up --build
```
This spins up:
- PostgreSQL database container on port `5432`
- FastAPI backend on `http://localhost:8000`
- React frontend on `http://localhost:5173`

---

## 11. How to Run Tests

OnboardIQ includes 12 automated unit and integration tests covering business logic, graph cycles, risk scoring, simulation isolation, approval enforcement, and the Alex Morgan demo scenario.

```bash
cd OnboardIQ/backend
# Activate virtual environment
# Windows: ..\venv\Scripts\activate  Unix: source ../venv/bin/activate

pytest -v
```

Expected output:
```
tests/test_approvals_and_execution.py::test_approval_rejection_prevents_execution PASSED
tests/test_approvals_and_execution.py::test_approval_and_automated_execution PASSED
tests/test_dependency_engine.py::test_cycle_detection PASSED
tests/test_dependency_engine.py::test_upstream_and_downstream_traversal PASSED
tests/test_dependency_engine.py::test_recalculate_task_statuses PASSED
tests/test_end_to_end_demo.py::test_full_alex_morgan_demo_workflow PASSED
tests/test_readiness_engine.py::test_readiness_calculation PASSED
tests/test_readiness_engine.py::test_readiness_blocked_penalty PASSED
tests/test_risk_engine.py::test_risk_clean_workflow PASSED
tests/test_risk_engine.py::test_risk_delayed_critical_task PASSED
tests/test_simulation_engine.py::test_simulation_ephemeral_isolation PASSED
tests/test_simulation_engine.py::test_recovery_optimizer_selection PASSED

====================== 12 passed in 1.80s ======================
```

---

## 12. Main End-to-End Demonstration Walkthrough

Follow this exact workflow to demonstrate OnboardIQ's core capabilities:

1. **Open Dashboard**:
   Navigate to `http://localhost:5173`. Select **Alex Morgan** (Software Developer, Engineering) in the top profile selector.
   - Note the Active Blockers alert and high initial risk score.

2. **Inspect Onboarding Workspace (`/workspace`)**:
   - Notice that `Identity Verification` (HR) is **Delayed** due to a pending passport scan re-upload.
   - Notice that `System Account Creation` (IT) and `Developer Environment Setup` (IT) are marked **Blocked**.

3. **View Dependency Graph (`/graph`)**:
   - The interactive React Flow diagram clearly displays the dependency chain.
   - Animated red edges trace from `Identity Verification` -> `System Account Creation` -> `Developer Environment Setup`.

4. **Review Risk & Root-Cause (`/risk`)**:
   - The Risk Engine shows an 78% risk score with an attention level of `Immediate Action Required`.
   - The Root-Cause diagnosis pinpoints `Identity Verification` as the root upstream bottleneck with a downstream blast radius of 2 technical tasks (+2.5 days schedule slippage).

5. **Launch What-If Simulator (`/simulator`)**:
   - The ephemeral simulation evaluates 3 recovery strategies in isolated memory:
     - **Scenario A**: Expedited Identity Verification (Priority HR Review) -> Saves 2.5 days, unblocks 2 tasks, boosts readiness to 84%.
     - **Scenario B**: Alternative Authorized IT Resource (Marcus Chen) -> Saves 1.5 days.
     - **Scenario C**: Reorder Independent Tasks -> Saves 1.0 day.
   - The **Recovery Optimizer** automatically selects **Scenario A** as the optimal intervention with the highest utility score.

6. **Approve Action (`/approvals`)**:
   - Manager Sarah Johnson reviews the proposed action, justification, and impact summary.
   - Click **Approve & Execute Self-Healing Action**.
   - The system dispatches to the mock Dayforce HR Gateway, updates the database, clears the blocker, and unblocks `System Account Creation`.

7. **Verify Dynamic Readiness Recalculation (`/readiness`)**:
   - The Day-1 Readiness score increases dynamically.
   - Critical path checklist updates in real-time.

8. **Review Continuous Learning (`/analytics`)**:
   - View historical bottleneck frequencies, prediction accuracy (MAE: 0.28 days), and recovery strategy success rates.

---

## 13. Mock Integrations & Limitations

- **Dayforce Hackathon Prototype**: All department APIs (HR, IT, Payroll, Benefits) are implemented as high-fidelity simulated mock gateways (`app/integrations/mock_apis.py`). They demonstrate realistic latency, payloads, and state mutations without connecting to proprietary production Dayforce endpoints.
- **LLM Integration**: Configured for local open-weights execution (e.g. Ollama `llama3`). A deterministic fallback demo mode is active by default to guarantee 100% operational reliability even if external model servers are offline.
- **Security Scope**: Includes role-based access control (Manager / HR Admin / Department User) and audit logging for hackathon demonstration purposes.
