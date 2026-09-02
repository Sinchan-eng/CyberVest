# AGENTS.md — CyberQuant AI Development Rulebook

## Project Identity

**Project:** CyberQuant AI  
**SIH Problem Statement:** SIH26105  
**Title:** AI-Powered Continuous Cyber Risk Quantification and Investment Optimization Platform  
**Domain:** Software

CyberQuant AI is a hackathon MVP, not a production enterprise cybersecurity platform.

The platform converts technical cybersecurity findings into financial risk metrics, identifies major risk contributors, recommends cost-effective mitigations, and optimizes cybersecurity investments under a fixed budget.

AI coding agents should prioritize a simple, demonstrable, explainable, and maintainable MVP over production-scale infrastructure or unnecessary complexity.

## Technology Stack

### Frontend

- React
- Vite
- TypeScript preferred
- Tailwind CSS
- Recharts
- Axios
- Lucide React

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

### Database

- SQLite for MVP

### AI

- Modular LLM integration
- Deterministic fallback when an external LLM is unavailable

### Optimization

- Python-based optimization using a greedy or knapsack-style approach as appropriate

## Architecture Rules

Use the following application flow:

```text
React frontend
    ↓
REST API
    ↓
FastAPI backend
    ↓
Business services
    ↓
SQLAlchemy
    ↓
SQLite
```

Rules:

- Keep business logic out of React components.
- Keep database logic separate from API route handlers.
- Keep risk calculations inside a dedicated risk engine.
- Keep investment optimization inside a dedicated optimizer.
- Keep AI functionality inside a dedicated AI service.
- Prefer clear boundaries between API schemas, business services, persistence, and presentation.
- Keep the architecture simple enough for a hackathon MVP.

## Coding Rules

1. Build incrementally.
2. Never implement the entire application in one step.
3. Read relevant documentation before modifying code.
4. Do not introduce unnecessary technologies.
5. Do not create microservices.
6. Do not use Kubernetes.
7. Do not add Kafka, Redis, Elasticsearch, or cloud infrastructure unless explicitly requested.
8. Do not rewrite unrelated working code.
9. Do not hardcode dashboard metrics.
10. Frontend metrics must ultimately come from backend APIs.
11. Use synthetic/demo data for the MVP.
12. Clearly label simulated data.
13. All risk calculations must be explainable.
14. Recommendations must include reasoning.
15. Preserve API contracts once established.
16. Use environment variables for secrets.
17. Never commit API keys.
18. Add validation for user inputs.
19. Handle API errors gracefully.
20. Maintain a clean and understandable folder structure.
21. Prefer simple solutions suitable for a hackathon.
22. Keep the application runnable after every change.

## Risk Calculation Rules

Never invent risk formulas silently.

All risk formulas must be documented in:

`docs/04-risk-engine.md`

Every financial risk number shown in the UI should be traceable to:

- input data
- calculation
- assumptions
- confidence/limitations where appropriate

When adding or changing a risk calculation:

- Update the risk-engine documentation before or alongside the implementation.
- Make assumptions explicit.
- Preserve enough intermediate values to explain how a result was produced.
- Avoid presenting simulated estimates as measured real-world financial losses.
- Ensure the UI can distinguish calculated values from assumptions and simulated/demo data.

## UI Rules

The UI should look like a professional cybersecurity/business intelligence product.

Prioritize:

- readability
- executive clarity
- financial metrics
- risk severity
- explainability
- responsive layouts
- useful empty/loading/error states

Avoid:

- excessive animations
- unnecessary gradients
- fake 3D graphics
- clutter
- meaningless decorative elements

Dashboard and analytical views should favor information density that supports decisions without sacrificing readability.

## MVP Rules

### Mandatory

- Synthetic assets
- Synthetic vulnerabilities
- Asset criticality
- Financial impact estimation
- Expected Annual Loss
- Enterprise financial exposure
- Risk contributors
- Recommendations
- Budget optimization
- ROSI
- Scenario simulation
- Executive dashboard
- Technical drill-down
- Natural-language risk query
- NIST CSF mapping

### Secondary

- VaR
- advanced ML
- additional framework mappings
- real SIEM/EDR integrations
- cloud deployment

Secondary capabilities must not delay or destabilize the mandatory MVP.

## Development Process

Before implementing a feature:

1. Read the relevant documentation.
2. Identify affected files.
3. Explain the implementation plan briefly.
4. Implement only the requested feature.
5. Run tests/build checks.
6. Report modified files and verification results.

Never silently expand scope.

The project documentation under `/docs` is the source of truth for:

- architecture
- data model
- APIs
- risk formulas
- UI requirements
- AI behavior
- optimization
- compliance mapping
- demo data
- development phases

When code and documentation conflict, inspect the relevant documentation first and resolve the discrepancy deliberately rather than silently choosing an implementation.

## Agent Working Principles

- Favor correctness, explainability, and demo reliability over abstraction for its own sake.
- Reuse existing utilities and patterns before creating new ones.
- Keep changes focused and reviewable.
- Avoid speculative features.
- Do not fabricate integrations, metrics, vulnerabilities, financial figures, or compliance claims.
- Use deterministic behavior for demos and tests wherever practical.
- If an external dependency or LLM is unavailable, use the documented fallback behavior rather than making the application fail unnecessarily.
- Keep synthetic data clearly separated from any future real-data integration path.
