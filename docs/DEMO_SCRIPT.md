# OnboardIQ 10-Minute Demo Script (Dayforce AI Innovation Challenge)

## Demo Overview
- **Presenter Role**: Senior Solutions Architect / Product Lead
- **Audience**: Dayforce AI Innovation Challenge Judges & Technical Reviewers
- **Focus**: What-If Simulator, Recovery Optimization, and Constraint-Aware Self-Healing Workflow

---

## 00:00 - 01:30 | Introduction & The Problem
- **Action**: Open the **Main Dashboard** (`http://localhost:5173`).
- **Script**:
  > "Hello everyone! Welcome to OnboardIQ: an Agentic AI-Powered Employee Onboarding Orchestrator built for the Dayforce AI Innovation Challenge.
  > 
  > Employee onboarding isn't just a checklist. It's an intricate, cross-functional choreography across HR, IT, Payroll, and Benefits. In traditional systems, when a task like 'Identity Verification' is delayed, the system merely marks it red. It has no idea that down in Engineering, the Developer Environment Setup is completely halted and the new hire won't be ready on Day 1.
  > 
  > OnboardIQ solves this by moving from passive tracking to active recovery. Let me show you how it works."

---

## 01:30 - 03:00 | The Candidate Profile & Coordinated Department Agents
- **Action**: Switch to **Alex Morgan** in the profile switcher or navigate to **Onboarding Workspace**.
- **Script**:
  > "Here is our candidate, Alex Morgan, joining as a Senior Software Developer in Engineering with manager Sarah Johnson.
  > 
  > Upon creation, OnboardIQ generated an AI-personalized onboarding plan specific to Engineering. Notice the four logical department agents at work: HR, IT, Payroll, and Benefits.
  > 
  > If we look at the tasks, 'Identity Verification' is delayed due to a re-submitted passport scan. Because of this, 'System Account Creation' and 'Developer Environment Setup' have automatically transitioned into a 'Blocked' state. Let's inspect the visual graph to see the architectural blast radius."

---

## 03:00 - 04:30 | Dynamic Dependency Graph & Blast Radius
- **Action**: Navigate to **Dependency Graph** (`/graph`).
- **Script**:
  > "This is OnboardIQ's real-time Dependency Graph engine, built with React Flow.
  > 
  > Notice that graph edges are not decorative—they are directed dependency constraints. The animated red edge clearly traces the failure path:
  > `Identity Verification (HR)` -> `System Account Creation (IT)` -> `Developer Environment Setup (IT)`.
  > 
  > Our deterministic graph engine has detected that two critical technical tasks are trapped downstream. If I click on any node, I can inspect who owns it, why it is blocked, and its SLA timeline."

---

## 04:30 - 06:00 | Predictive Delay & AI Root-Cause Analysis
- **Action**: Navigate to **Risk & Root-Cause** (`/risk`).
- **Script**:
  > "On our Risk Engine page, OnboardIQ has computed an overall risk score of 78% (Critical).
  > 
  > Rather than guessing, the Root-Cause engine deterministically traced the upstream dependency chain to pinpoint the original bottleneck: 'Identity Verification'.
  > 
  > It quantifies the downstream blast radius: 2 technical tasks halted, with a projected Day-1 schedule slippage of +2.5 business days.
  > 
  > But knowing there is a problem is only half the battle. Now comes our biggest differentiator: The What-If Simulator."

---

## 06:00 - 08:00 | What-If Simulation & Recovery Optimization (Flagship Innovation)
- **Action**: Navigate to **What-If Simulator** (`/simulator`).
- **Script**:
  > "Welcome to the What-If Simulator. In a live enterprise, HR and managers cannot just test random actions in production.
  > 
  > OnboardIQ creates an isolated ephemeral sandbox—a cloned snapshot of the task graph that evaluates hypothetical interventions without mutating persistent records:
  > 
  > - **Scenario A (Expedited Identity Verification)**: Simulates completing HR verification immediately today via priority review. It unblocks 2 downstream tasks and saves 2.5 days.
  > - **Scenario B (Alternative Authorized IT Resource)**: Simulates assigning Level-2 DevOps Admin Marcus Chen to stage credentials in parallel under a staging waiver.
  > - **Scenario C (Reorder Independent Tasks)**: Prioritizes Payroll direct deposit and Benefits enrollment while technical tasks wait.
  > 
  > Our **Recovery Optimizer** analyzes all three scenarios using a multi-criteria utility formula factoring time saved, tasks unblocked, readiness delta, and policy compliance.
  > 
  > Scenario A wins with the highest utility score because it resolves the root upstream bottleneck and ensures 100% regulatory compliance. Let's submit this optimal strategy for manager authorization."

---

## 08:00 - 09:15 | Human-in-the-Loop Approval & Self-Healing Execution
- **Action**: Click **Review & Approve Action**, navigating to **Recovery & Approvals** (`/approvals`).
- **Script**:
  > "Here in the Manager Approval Center, Sarah Johnson reviews the proposed self-healing action:
  > The system displays the justification, the affected tasks, and the expected impact.
  > 
  > Notice that rejected actions can never execute, protecting compliance integrity.
  > 
  > Now, I will click **Approve & Execute Self-Healing Action**.
  > 
  > Behind the scenes, OnboardIQ dispatches to the mock Dayforce HRIS Gateway. The database updates in real-time: 'Identity Verification' is marked Completed, and downstream 'System Account Creation' is instantly unblocked!"

---

## 09:15 - 10:00 | Dynamic Readiness Recalculation & Continuous Learning
- **Action**: Navigate to **Readiness Dashboard** (`/readiness`) and then **Learning & Analytics** (`/analytics`).
- **Script**:
  > "Look at our Day-1 Readiness Dashboard! The readiness score has jumped dynamically, reflecting that our critical path is back on schedule.
  > 
  > Finally, in our **Learning & Analytics** center, every simulated intervention and approved outcome is recorded in our historical ledger.
  > 
  > OnboardIQ tracks prediction accuracy (MAE: 0.28 days), analyzes recurring department bottlenecks, and continually refines future recommendations based on past success rates.
  > 
  > That is OnboardIQ: from static checklists to intelligent, autonomous onboarding orchestration. Thank you!"
