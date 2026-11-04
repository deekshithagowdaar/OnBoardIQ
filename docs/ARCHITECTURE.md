# OnboardIQ System Architecture & Engineering Design

## 1. Architectural Philosophy & Overview
OnboardIQ is an **Agentic AI-Powered Employee Onboarding Orchestrator** engineered for the Dayforce AI Innovation Challenge. 

While conventional HRIS systems passively display checklists and pending task statuses, OnboardIQ functions as an active recovery and workflow optimization engine. It continuously tracks cross-departmental dependency DAGs (Directed Acyclic Graphs), detects upstream delay propagation, quantifies downstream blast radii, simulates alternative recovery interventions in isolated ephemeral sandboxes, and executes manager-approved self-healing workflows via department gateways.

```
                                  +---------------------------------------+
                                  |   New Employee Profile (Module 1)     |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  | AI Personalized Onboarding Plan (M2)  |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                     +-----------------------------------------------------------------+
                     |            Multi-Agent Department Coordination (M3)             |
                     |   (HR Agent, IT Agent, Payroll Agent, Benefits Agent via LangGraph)   |
                     +--------------------------------+--------------------------------+
                                                      |
                                                      v
                     +-----------------------------------------------------------------+
                     |        Dynamic Dependency Graph & Real-Time Monitoring (M4)     |
                     |               (Adjacency Lists, Cycle Detection, DAG)           |
                     +--------------------------------+--------------------------------+
                                                      |
                                                      v
                     +-----------------------------------------------------------------+
                     |              Predictive Delay & Risk Detection (M5)             |
                     |         (Explainable 0-100 Risk Scoring, Delay Propagation)     |
                     +--------------------------------+--------------------------------+
                                                      |
                                                      v
                     +-----------------------------------------------------------------+
                     |       AI Root-Cause & Downstream Blast Radius Analysis (M6)     |
                     |            (Pinpoints Root Bottleneck & Downstream Halt)        |
                     +--------------------------------+--------------------------------+
                                                      |
                                                      v
                     +-----------------------------------------------------------------+
                     |      Onboarding What-If Simulation & Recovery Optimization (M7)  |
                     |     (Ephemeral Cloned Graph Sandbox, Multi-Criteria Optimizer)  |
                     +--------------------------------+--------------------------------+
                                                      |
                                                      v
                     +-----------------------------------------------------------------+
                     |         Constraint-Aware Self-Healing Workflow (M8)             |
                     |    (Policy Verification, Fast-Track Rules, Compliance Guardrails)|
                     +--------------------------------+--------------------------------+
                                                      |
                                                      v
                     +-----------------------------------------------------------------+
                     |          Manager Approval for Critical Actions (M9)             |
                     |        (Human-in-the-Loop Checkpoints, RBAC, Audit Logging)     |
                     +--------------------------------+--------------------------------+
                                                      |
                                                      v
                     +-----------------------------------------------------------------+
                     |     Automated Action Execution & Workflow Adaptation (M10)      |
                     |        (Mock HR/IT/Payroll APIs, In-Place State Unblocking)     |
                     +--------------------------------+--------------------------------+
                                                      |
                                                      v
                     +-----------------------------------------------------------------+
                     |             Dynamic Onboarding Readiness Score (M11)            |
                     |            (Explainable 4-Factor Mathematical Formulation)      |
                     +--------------------------------+--------------------------------+
                                                      |
                                                      v
                     +-----------------------------------------------------------------+
                     |        Continuous Learning from Onboarding Outcomes (M12)       |
                     |          (Bottleneck Analytics, MAE Accuracy, Strategy Success) |
                     +-----------------------------------------------------------------+
```

---

## 2. Multi-Agent Department Coordination (LangGraph)
OnboardIQ implements four dedicated logical department agents orchestrated through a compiled **LangGraph `StateGraph`**:
- **HR Agent**: Audits identity verification, I-9 compliance forms, employee NDAs, and flags non-compliance.
- **IT Agent**: Monitors system credential provisioning, SSO email generation, laptop logistics, and developer sandbox environments.
- **Payroll Agent**: Verifies direct deposit void checks, tax withholding (W-4) schedules, and payroll registry synchronization.
- **Benefits Agent**: Tracks health, dental, vision, and 401(k) election windows.

Each agent maintains distinct tools and domain responsibilities, communicating task state to the central `WorkflowState` without unnecessary LLM hallucination for database queries.

---

## 3. Dynamic Dependency Graph Engine
The core graph engine (`app/engine/dependency_engine.py`) operates strictly on deterministic algorithms:
- **Cycle Detection**: Depth-First Search with recursion call-stack tracking ensures that circular dependencies can never be persisted or introduced by users.
- **Upstream Blocker Tracing**: Traverses reverse dependency edges recursively to pinpoint the exact root prerequisite stalling a workflow.
- **Downstream Blast Radius**: Traverses forward adjacency lists to calculate every downstream task transitively blocked.
- **Automated Blocked State Recalculation**: Tasks automatically transition between `Blocked` and `Pending` in real-time as prerequisites are satisfied.
- **Interactive UI**: Formatted into React Flow node and edge definitions with custom styling, animated red edges for blocked dependency paths, and auto-hierarchical rank layout.

---

## 4. Ephemeral What-If Simulation Sandbox
A key hackathon innovation is the **What-If Simulation Engine** (`app/engine/simulation_engine.py`):
- Operates on deep-copied ephemeral task graph snapshots in memory.
- Guarantees **zero side-effects or mutations** on production database records while simulating hypothetical interventions.
- Simulates standard Scenarios A, B, and C as well as custom user configurations:
  - **Scenario A (Expedited Identity Verification)**: Clears upstream compliance blocker, unblocking 2 downstream technical tasks, saving 2.5 days, and boosting readiness from 36% to 84%.
  - **Scenario B (Alternative Authorized IT Resource)**: Assigns Marcus Chen (Senior DevOps Lead) to fast-track account staging in parallel under policy waiver.
  - **Scenario C (Reorder Independent Tasks)**: Accelerates non-blocking Payroll & Benefits workflows to maintain onboarding momentum.
- **Recovery Optimizer (`app/engine/recovery_optimizer.py`)**: Computes a multi-criteria utility score incorporating time saved, tasks unblocked, readiness score improvement, and compliance adherence to automatically rank and recommend the optimal recovery plan.

---

## 5. Explainable Readiness Score Formula
The Onboarding Readiness Score (0 to 100) avoids opaque black-box calculations by using an explainable 4-factor formula:
$$\text{Readiness} = (0.35 \times \text{CompletionRatio}) + (0.25 \times \text{CriticalPathHealth}) + (0.20 \times \text{DepartmentParity}) + (0.20 \times \text{TimelineHealth})$$
- **Completion Ratio (35%)**: Proportion of completed tasks to total plan tasks.
- **Critical Path Health (25%)**: Status of Day-1 critical requirements, with severe deductions for stalled critical tasks.
- **Department Parity (20%)**: Balanced completion across HR, IT, Payroll, and Benefits.
- **Timeline / Blocker Health (20%)**: Deductions based on active blocker count and days remaining before joining date.

---

## 6. Database Relational Design (PostgreSQL / SQLite Fallback)
The database architecture provides 14 relational tables with primary keys, foreign key constraints, and indices:
- `employees`: Core candidate profiles, roles, locations, equipment, and compliance requirements.
- `departments`: Organizational business units and department heads.
- `users`: Role-based access control (`HR_ADMIN`, `MANAGER`, `DEPARTMENT_USER`).
- `onboarding_plans`: Personalized onboarding trajectories.
- `tasks`: Individual onboarding activities with priority, duration, dates, and status.
- `task_dependencies`: Directed edges forming the onboarding DAG.
- `risk_predictions`: Historical records of calculated risk scores and factors.
- `root_cause_analyses`: Diagnosed root bottlenecks and blast radius calculations.
- `simulation_scenarios`: Ephemeral simulation records and evaluation results.
- `recovery_recommendations`: Optimal recovery rankings and justifications.
- `approval_requests`: Human-in-the-loop authorization queue for managers.
- `action_executions`: Audit trail of executed self-healing interventions.
- `readiness_snapshots`: Periodic snapshots of readiness scores.
- `historical_outcomes`: Training ledger for continuous learning and bottleneck analytics.
