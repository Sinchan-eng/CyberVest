# CyberQuant AI — Development Plan

> **Status:** Authoritative phased implementation plan  
> **Objective:** Build CyberQuant AI incrementally into a working, integrated hackathon MVP  
> **Rule:** Do not skip directly to later phases. Complete, test, build, verify, and document each phase before moving forward.

---

## 1. Development Strategy

CyberQuant AI must be implemented in small, verifiable phases.

The project should prioritize:

- working end-to-end functionality
- deterministic and explainable risk calculations
- API-driven frontend data
- simulated enterprise data clearly labeled as simulated
- modular code that can be extended later
- reliable demo behavior over unnecessary production complexity

The intended development path is:

```text
Foundation
→ Database
→ Risk Engine
→ APIs
→ Executive Dashboard
→ Technical Drill-Down
→ Investment Optimizer
→ Scenario Simulator
→ AI Assistant
→ Compliance
→ UX Polish
→ Full Testing
→ SIH Demo Preparation
```

Each phase must preserve all previously working behavior.

---

# Phase 1 — Project Foundation

## Goal

Create the minimum working frontend/backend project structure.

## Backend

Set up:

- FastAPI backend
- Python virtual environment
- dependency management
- application entry point
- configuration module
- CORS configuration
- structured backend folder layout
- health-check endpoint

Recommended backend structure:

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── risk/
│   ├── optimizer/
│   ├── ai/
│   └── compliance/
├── tests/
└── requirements.txt
```

Minimum endpoint:

```http
GET /api/health
```

Example response:

```json
{
  "status": "ok"
}
```

## Frontend

Set up:

- React
- Vite
- TypeScript
- Tailwind CSS
- Axios
- Recharts
- Lucide React
- base application routing
- global styles
- basic application shell

Recommended frontend structure should follow `docs/06-frontend-specification.md`.

## Environment Configuration

Create environment configuration for at least:

```text
VITE_API_BASE_URL
DATABASE_URL
APP_ENV
```

Do not hardcode deployment-specific URLs.

## Acceptance Criteria

Phase 1 is complete when:

- frontend starts successfully
- backend starts successfully
- frontend can call the health-check API
- CORS works
- environment variables are loaded correctly
- project folder structure exists
- frontend and backend builds/startups have no blocking errors

---

# Phase 2 — Database

## Goal

Create a deterministic synthetic enterprise dataset backed by SQLite.

## Implement

- SQLAlchemy
- SQLite
- database session management
- database initialization
- database models
- seed data
- migrations only if necessary for the MVP

## Minimum Models

Implement models for at least:

- Asset
- Vulnerability/Finding
- SecurityControl
- RiskRecord or calculated-risk persistence if needed
- Recommendation/InvestmentOption
- ComplianceMapping
- Scenario metadata where appropriate

The exact models must align with the API and risk specifications.

## Asset Data

Seed assets with:

- id
- name
- type
- business unit
- criticality
- financial value
- downtime cost
- internet exposure
- data sensitivity
- control effectiveness

## Vulnerability Data

Seed vulnerabilities with:

- id
- CVE where applicable
- name/description
- affected asset
- CVSS
- exploitability
- threat activity
- severity
- status

Never invent a CVE identifier in runtime AI responses. Seeded demo CVEs must be explicit source data.

## Synthetic Data Requirement

All demo records must clearly be treated as:

```text
SIMULATED
```

The system must not imply that these are real enterprise findings.

## Acceptance Criteria

Phase 2 is complete when:

- SQLite initializes successfully
- seed script runs successfully
- synthetic assets exist
- synthetic vulnerabilities exist
- relationships resolve correctly
- data can be queried through SQLAlchemy
- database setup is reproducible from a clean environment

---

# Phase 3 — Risk Engine

## Goal

Implement the authoritative deterministic risk engine from `docs/04-risk-engine.md`.

## Implement

### Probability

Implement:

- CVSS normalization
- base probability
- risk adjustment factors
- probability bounds
- control-effectiveness reduction

All formulas must exactly match the authoritative risk specification.

### Financial Impact

Implement:

```text
Financial Impact =
Downtime Cost
+ Data Breach Cost
+ Recovery Cost
+ Regulatory Cost
+ Reputation/Business Impact
```

Do not silently fabricate missing financial values.

### Expected Annual Loss

Implement:

```text
EAL = Incident Probability × Financial Impact
```

### Enterprise Aggregation

Implement:

```text
Enterprise Exposure = sum of canonical asset/risk EAL values
```

Avoid double-counting.

### Enterprise Risk Score

Implement the normalized 0–100 score exactly as defined in the risk specification.

### Explainability

Every calculated risk result should expose:

- raw inputs
- normalized inputs
- base probability
- adjustment multiplier
- pre-control probability
- final incident probability
- financial-impact components
- financial impact
- EAL
- major risk drivers
- confidence/data completeness
- assumptions

## Testing

Create unit tests using the normative examples from `docs/04-risk-engine.md`.

Must include:

- CVSS = 0
- CVSS = 10
- 0% control effectiveness
- 50% control effectiveness
- 100% control effectiveness
- financial impact example
- missing financial data
- enterprise aggregation
- risk-score boundaries

## Acceptance Criteria

Phase 3 is complete when:

- all authoritative numerical examples match expected outputs
- all unit tests pass
- results are deterministic
- probabilities always remain between 0 and 1
- explainability output is available
- missing financial data does not result in invented EAL values

---

# Phase 4 — API

## Goal

Expose real backend data and calculated risk information to the frontend.

## Implement

At minimum:

### Dashboard API

```http
GET /api/dashboard
```

Return:

- enterprise risk score
- total financial exposure
- enterprise EAL
- critical assets count
- critical vulnerabilities count
- risk trend where available
- top contributors
- risk reduction opportunities
- last updated
- simulated/live status

### Assets API

```http
GET /api/assets
GET /api/assets/{asset_id}
```

### Vulnerabilities API

```http
GET /api/vulnerabilities
GET /api/vulnerabilities/{vulnerability_id}
```

### Risks API

Expose:

- calculated risk records
- risk detail
- explainability
- major risk drivers

### Recommendations API

Expose:

- remediation recommendations
- priority
- cost
- estimated risk reduction
- related assets/risks

## API Rules

- use JSON
- validate request inputs
- use consistent error responses
- use backend calculations as source of truth
- never send hardcoded metrics from route handlers
- return simulated/live metadata where relevant

## Acceptance Criteria

Phase 4 is complete when:

- frontend can retrieve backend data
- endpoints return seeded database records
- dashboard metrics are calculated from backend data
- no business metric exists only as hardcoded frontend data
- invalid IDs return appropriate errors
- API responses match the documented contracts

---

# Phase 5 — Executive Dashboard

## Goal

Build the main executive experience using real API data.

## Implement

### KPI Cards

Show:

- Enterprise Risk Score
- Total Financial Exposure
- Expected Annual Loss
- Critical Assets
- Critical Vulnerabilities

### Risk Trend

Render API-provided trend data with Recharts.

If no trend data exists, show an empty state.

Do not fabricate a historical series.

### Top Contributors

Show:

- top financial-risk assets/findings
- EAL/exposure
- major drivers
- severity
- affected business unit

### Critical Assets

Surface the most important critical assets.

### Recommendations

Show risk-reduction opportunities from the recommendation API.

### Metadata

Show:

- Last Updated
- SIMULATED/LIVE indicator

## Acceptance Criteria

Phase 5 is complete when:

- every dashboard metric comes from an API
- no dashboard KPI is hardcoded
- loading states work
- errors display correctly
- empty data does not display fake values
- navigation to asset/risk detail works

---

# Phase 6 — Technical Drill-Down

## Goal

Allow analysts to move from enterprise risk to technical evidence.

## Implement

### Assets

Build:

- asset table
- search
- filtering
- sorting where useful
- asset detail

### Vulnerabilities

Build:

- vulnerability table
- CVSS
- severity
- probability
- financial impact
- EAL
- affected asset

### Risk Details

Display:

- incident probability
- financial impact
- EAL
- confidence
- major risk drivers
- mitigation recommendations

### Explainability

Implement the explainability panel from the frontend specification.

Show:

```text
Technical Finding
→ Base Probability
→ Adjustment Factors
→ Control Effectiveness
→ Incident Probability
→ Financial Impact
→ EAL
```

## Acceptance Criteria

Phase 6 is complete when:

- user can select an asset
- user can inspect its vulnerabilities
- user can inspect financial risk
- user can view major risk drivers
- user can view calculation inputs/intermediate values
- frontend does not independently recalculate authoritative risk values

---

# Phase 7 — Investment Optimizer

## Goal

Recommend the best set of remediation/control investments under a fixed budget.

## Backend

Implement the investment optimization engine according to the investment specification.

Inputs should include:

- option id
- name
- description
- cost
- affected assets
- affected risks
- expected risk reduction
- implementation time
- priority

Constraint:

```text
Total Selected Investment Cost <= Budget
```

For the MVP, use a deterministic optimization approach such as:

- 0/1 knapsack
- bounded enumeration
- deterministic cost-benefit selection where appropriate

Do not substitute an undocumented heuristic if a deterministic optimizer is feasible.

## ROSI

Use the documented ROSI definition from the investment specification.

Do not invent a second ROSI formula in the frontend.

## Frontend

Implement:

- budget input
- recommended controls
- control cost
- risk reduction
- ROSI
- total spend
- remaining budget
- investment-vs-risk-reduction chart

## Acceptance Criteria

Phase 7 is complete when:

- user enters an INR budget
- selected investment cost never exceeds the budget
- results are deterministic
- recommended controls come from backend logic
- risk reduction is returned by backend
- ROSI is returned by backend
- frontend does not calculate business metrics independently

---

# Phase 8 — Scenario Simulator

## Goal

Show how security changes affect modeled financial exposure.

## Implement

Allow selection/change of:

- control effectiveness
- vulnerability status
- exposure
- remediation status
- mitigation actions

The scenario engine must use the **same canonical risk pipeline** as normal calculations.

Do not create separate scenario risk formulas.

## Results

Return and display:

- baseline exposure
- scenario exposure
- absolute reduction
- percentage reduction
- affected assets
- affected findings
- assumptions

## Visualization

Implement a clear before/after comparison.

## Acceptance Criteria

Phase 8 is complete when:

- user can select at least one mitigation
- scenario uses the canonical risk engine
- before and after values are returned by backend
- absolute reduction is correct
- percentage reduction is correct
- baseline data is not mutated by a simulation
- results are reproducible

---

# Phase 9 — AI Assistant

## Goal

Provide grounded natural-language risk decision support.

Follow `docs/07-ai-decision-engine.md`.

## Implement

### Natural-Language Query

Support at least:

- highest financial cyber risk
- vulnerability contributing most to expected loss
- most exposed asset
- what to fix first
- risk reduction under a specified budget

### Deterministic Fallback

Implement:

- intent classification
- entity/parameter extraction
- structured backend retrieval
- deterministic response construction
- grounding validation

The MVP must work without an external LLM.

### Optional LLM Integration

Create a provider abstraction so a later external LLM can be added.

The external LLM must not become authoritative for:

- EAL
- probabilities
- financial impact
- exposure
- optimizer outputs
- compliance status

### Explainable Answers

Responses should include:

- Answer
- Key Evidence
- Risk Drivers
- Recommendation
- Estimated Impact
- Confidence / Limitations

## Guardrails

Verify that the AI:

- does not invent CVEs
- does not invent financial values
- does not invent compliance mappings
- distinguishes simulated data from live telemetry
- distinguishes modeled estimates from facts
- reports missing data
- avoids guaranteed-outcome language

## Acceptance Criteria

Phase 9 is complete when:

- required natural-language questions work
- deterministic fallback works with no external LLM
- answers are grounded in structured backend data
- response values match source data
- synthetic data is identified
- unsupported questions fail safely

---

# Phase 10 — Compliance

## Goal

Demonstrate cybersecurity-framework mapping.

## MVP Scope

Implement:

**NIST CSF**

## Backend

Create:

- framework control records
- mapping between CyberQuant AI controls/findings and NIST CSF
- mapping status
- supporting evidence

Statuses:

- Mapped
- Partially Mapped
- Unmapped

## Frontend

Build:

- compliance table
- search
- filter by mapping status
- coverage summary/dashboard
- mapped evidence/detail view

## Acceptance Criteria

Phase 10 is complete when:

- NIST CSF records load from backend
- selected controls can be linked to mappings
- coverage can be displayed
- mapping status is never invented by the AI/frontend
- compliance data is API-driven

---

# Phase 11 — Polish

## Goal

Make the integrated MVP reliable and demo-ready.

## Implement

### Loading States

Add:

- skeleton cards
- skeleton tables
- chart placeholders
- assistant loading indicators

### Error Handling

Handle:

- network failures
- API validation failures
- missing data
- unavailable AI provider
- scenario failure
- optimizer failure

### Empty States

Provide clear empty states for:

- assets
- vulnerabilities
- recommendations
- scenarios
- compliance
- risk trends

Never substitute fake content.

### Responsive UI

Verify:

- desktop
- laptop
- tablet
- mobile

### Data Refresh

Implement:

- manual refresh where appropriate
- last-updated timestamp
- stable state during refresh

### Demo Mode

Ensure:

- dataset status is visibly SIMULATED
- demo dataset can be reset/reseeded
- demo results are deterministic
- no external service is required for core demo flow

### Final UX Polish

Improve:

- typography
- spacing
- cards
- tooltips
- accessibility
- table readability
- severity indicators
- INR formatting
- chart labels

## Acceptance Criteria

Phase 11 is complete when:

- all major views have loading/error/empty states
- the application works on common screen sizes
- simulated data is clearly identified
- demo data is repeatable
- no raw stack traces appear in the UI
- no broken navigation remains

---

# Phase 12 — Testing

## Goal

Verify the complete integrated system before SIH demo preparation.

## Risk Formula Tests

Test:

- probability
- bounds
- control effectiveness
- financial impact
- EAL
- aggregation
- risk score
- confidence
- explainability

## Optimizer Tests

Test:

- budget constraint
- deterministic output
- zero budget
- budget smaller than cheapest option
- budget sufficient for all options
- ROSI
- risk reduction

## API Tests

Test:

- success cases
- invalid IDs
- invalid payloads
- validation
- error schema
- scenario endpoint
- optimizer endpoint
- assistant endpoint

## Database Tests

Test:

- seed data
- relationships
- initialization
- clean recreation
- constraints

## Frontend Tests

Verify:

- build succeeds
- API integration works
- routing works
- loading states
- error states
- empty states
- responsive layouts
- data-status indicator

## Scenario Tests

Verify:

- before/after values
- absolute reduction
- percentage reduction
- baseline immutability
- canonical risk pipeline reuse

## AI Fallback Tests

Verify:

- supported intents
- deterministic output
- correct entity selection
- grounded metrics
- no invented CVEs
- no invented financial values
- simulated/live labeling
- missing-data behavior

## Acceptance Criteria

Phase 12 is complete when:

- all critical unit tests pass
- all API tests pass
- frontend production build passes
- known risk-engine examples match the specification
- optimizer respects all constraints
- scenario outputs are correct
- AI fallback is grounded and deterministic
- no regression breaks earlier phases

---

# Phase 13 — SIH Demo Preparation

## Goal

Prepare a concise, reliable presentation of the complete CyberQuant AI MVP.

## 13.1 Architecture Diagram

Prepare a clear architecture covering:

```text
Data Sources
→ Ingestion
→ Database / Normalization
→ Risk Engine
→ Investment Optimizer
→ AI Decision Layer
→ Compliance Mapping
→ APIs
→ React Frontend
```

Clearly distinguish MVP implementation from future enterprise architecture.

## 13.2 Problem Statement

Explain:

- organizations use qualitative cyber-risk ratings
- technical vulnerabilities are difficult to connect to business impact
- executives cannot easily understand financial exposure
- security budgets are difficult to optimize objectively

## 13.3 Solution Explanation

Explain CyberQuant AI as:

> **A platform that turns cyber risk into business language and turns security spend into an optimization problem.**

## 13.4 Live Demo Flow

Recommended demo:

```text
Open Dashboard
→ Show SIMULATED data indicator
→ Show enterprise financial exposure
→ Identify highest financial risk
→ Drill into critical asset
→ Show vulnerability
→ Explain probability and EAL
→ Show recommended mitigation
→ Enter security budget
→ Run optimizer
→ Show selected controls and ROSI
→ Run scenario
→ Show reduced exposure
→ Ask AI: "What should we fix first?"
→ Show grounded response
→ Show NIST CSF mapping
```

## 13.5 Before/After Scenario

Prepare one deterministic scenario with a clear story.

For example:

```text
Before:
High control weakness
High exposure
Higher EAL

Mitigation:
Apply selected control

After:
Improved control effectiveness
Lower modeled probability
Lower EAL
```

All demo values must come from the application.

## 13.6 Investment Optimization Story

Clearly explain:

- fixed budget
- competing security investments
- risk-reduction values
- optimizer constraint
- recommended selection
- remaining budget
- ROSI

## 13.7 Limitations

State openly:

- data is simulated for the hackathon
- probability model is transparent but not actuarially calibrated
- financial estimates depend on input quality
- MVP uses SQLite
- integrations are simulated/limited
- recommendations support human decisions
- LLM integration is optional
- no automated production remediation is performed

## 13.8 Future Roadmap

Possible future work:

- live SIEM/EDR/vulnerability integrations
- CMDB integration
- threat-intelligence feeds
- cloud-native deployment
- PostgreSQL
- event streaming
- calibrated probability models
- organization-specific financial models
- additional compliance frameworks
- richer LLM/RAG layer
- historical risk trends
- approval workflows
- continuous monitoring

## Acceptance Criteria

Phase 13 is complete when:

- demo can be run end-to-end from a clean startup
- architecture diagram is ready
- problem and solution are clear
- financial-risk story is understandable
- optimizer story works
- scenario story works
- AI assistant works without requiring an external LLM
- limitations are explicit
- future roadmap is prepared

---

# 14. Mandatory Development Rules

These rules apply to every phase.

## 14.1 Do Not Skip Phases

Do not jump directly to:

- AI
- optimizer
- dashboards
- compliance

before the required underlying database, risk engine, and APIs are working.

Later features must build on validated earlier layers.

## 14.2 MVP Before Advanced Features

Do not implement advanced production infrastructure before the MVP works.

Examples of features that should **not** block the MVP:

- Kubernetes
- distributed streaming
- complex microservices
- enterprise IAM
- large-scale event pipelines
- multi-region deployment
- complex ML training pipelines
- production-grade observability stacks

These may be future roadmap items.

## 14.3 API-Driven Metrics

Do not hardcode business metrics in the frontend.

Metrics such as:

- EAL
- risk score
- exposure
- risk reduction
- ROSI
- asset counts
- vulnerability counts

must come from backend APIs.

## 14.4 Authoritative Risk Engine

All risk calculations must follow `docs/04-risk-engine.md`.

Do not create alternate formulas in:

- frontend
- AI assistant
- optimizer presentation layer
- scenario UI

## 14.5 Grounded AI

All organization-specific AI claims must come from structured backend data.

Do not invent missing values.

## 14.6 Simulated Data Labeling

All hackathon synthetic data must be clearly labeled:

```text
SIMULATED
```

Never imply simulated findings represent a real enterprise.

---

# 15. Required Phase Completion Routine

After **every phase**, perform these four actions:

## 1. Run Tests

Run all existing tests relevant to the project.

Do not only run tests added in the current phase.

## 2. Run Build

Verify:

- backend starts
- frontend builds
- frontend starts
- TypeScript compilation succeeds

## 3. Verify Existing Features

Regression-check previously completed phases.

Example:

After implementing the optimizer, verify that:

- dashboard still works
- asset drill-down still works
- risk calculations remain unchanged

## 4. Document Changes

Update:

- relevant docs
- README/setup instructions where necessary
- API documentation if contracts changed
- assumptions
- known limitations

Do not allow implementation behavior and documentation to silently diverge.

---

# 16. Recommended Git Milestones

Use one stable milestone per completed phase.

Suggested tags/branches:

```text
phase-01-foundation
phase-02-database
phase-03-risk-engine
phase-04-api
phase-05-dashboard
phase-06-drilldown
phase-07-optimizer
phase-08-scenarios
phase-09-ai
phase-10-compliance
phase-11-polish
phase-12-tested-mvp
phase-13-sih-demo
```

Each milestone should represent a working state.

---

# 17. MVP Critical Path

If development time becomes constrained, prioritize this path:

```text
Foundation
→ Database
→ Risk Engine
→ Dashboard API
→ Executive Dashboard
→ Asset/Risk Drill-Down
→ Investment Optimizer
→ Scenario Simulator
→ Deterministic AI Query
→ NIST CSF Mapping
→ Demo Polish
```

Do not sacrifice deterministic core calculations for optional visual or infrastructure complexity.

---

# 18. Final Definition of Done

The CyberQuant AI hackathon MVP is ready when a judge can:

1. Start the frontend and backend successfully.
2. See clearly labeled simulated enterprise data.
3. View enterprise financial exposure and EAL.
4. Identify the largest financial-risk contributor.
5. Drill into an asset and vulnerability.
6. See why the risk is high.
7. Inspect the risk calculation explanation.
8. Enter a fixed security budget.
9. Receive optimized remediation/control recommendations.
10. View ROSI and estimated risk reduction.
11. Run a scenario.
12. Compare before and after financial exposure.
13. Ask the AI assistant what should be fixed first.
14. Receive a grounded, explainable answer.
15. View NIST CSF mapping.
16. Understand the limitations of the MVP.
17. See a clear roadmap toward a production implementation.

---

# 19. Guiding Principle

The project should always favor a small integrated system that works over a large architecture that is only partially implemented.

> **Build the complete decision loop first: data → risk → financial impact → prioritization → investment → scenario → explanation.**

That loop is the CyberQuant AI MVP.
