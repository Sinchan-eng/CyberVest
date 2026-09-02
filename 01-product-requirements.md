# CyberQuant AI — Product Requirements

**Project:** CyberQuant AI  
**SIH Problem Statement:** SIH26105  
**Source:** SIH26105 Product Requirements Document (PRD), Version 1.0  
**Status:** MVP implementation requirements for the hackathon

## 1. Purpose and MVP interpretation

CyberQuant AI converts technical cybersecurity findings into business-oriented financial risk metrics, identifies major risk contributors, recommends cost-effective mitigations, and helps optimize cybersecurity investment under a fixed budget.

The MVP translates the PRD functional requirements into a small, demonstrable implementation. The PRD remains the source of truth; this document makes its requirements concrete without turning the hackathon MVP into a production SIEM, EDR, vulnerability scanner, or automated remediation platform.

The MVP should use simulated/sample data for the demonstration, while keeping interfaces structured so future connectors can replace the sample inputs.

### MVP boundaries

- Ingest simulated/sample data representing an asset inventory, vulnerability findings, and a security/telemetry source.
- Calculate explainable financial risk at asset and enterprise level.
- Provide prioritized recommendations and scenario analysis.
- Optimize remediation/control investments for a supplied budget.
- Provide an executive dashboard and technical drill-down.
- Prioritize NIST CSF mapping for the MVP.
- Keep ISO 27001, CIS Controls, RBI CSF, and SEBI CSCRF behind a modular framework-mapping interface for later implementation.
- Do not auto-patch, auto-configure, or otherwise execute remediation.
- Do not replace SIEM/EDR/scanners.
- Do not present simulated financial estimates as measured real-world losses.

---

# Risk Quantification

## RQ-1. Asset inventory

The system shall maintain a normalized inventory of assets used by the risk engine.

### MVP requirements

Each asset shall support, at minimum:

- unique asset ID
- asset name
- asset type/category
- business unit or organizational grouping
- criticality
- financial impact inputs
- associated vulnerabilities/findings
- associated controls where available
- service/dependency relationships where represented by demo data

The ingestion model shall allow sample asset-inventory data to be loaded without requiring a live CMDB integration.

## RQ-2. Vulnerability data

The system shall ingest and normalize vulnerability findings associated with assets.

A vulnerability finding shall support:

- vulnerability/finding ID
- affected asset
- severity
- description/title
- status
- relevant exposure/threat factors when available
- remediation/action association when available

For the MVP, scanner data may be simulated. The normalized schema shall not depend on one scanner vendor.

## RQ-3. Asset criticality

The system shall assign an asset criticality value that represents business importance.

Criticality shall influence risk calculations so that the same technical finding can produce different business risk on assets of different importance.

The MVP may use a bounded, documented criticality scale rather than a complex dependency-graph model, provided the calculation is explicit and traceable.

## RQ-4. Vulnerability severity

The system shall normalize vulnerability severity into a documented scale.

Severity shall affect incident probability and/or risk scoring in a deterministic, explainable manner.

The implementation shall preserve the original severity when supplied and the normalized value used by the risk engine.

## RQ-5. Threat/exposure factors

The system shall support threat and exposure factors that modify baseline incident probability.

MVP factors may include, where supported by the simulated data:

- external exposure
- active exploitation/threat signal
- asset exposure
- vulnerability severity
- relevant security telemetry

Each factor and its effect on the adjusted probability must be visible in the calculation explanation.

The MVP shall not claim predictive threat intelligence capabilities beyond the available inputs.

## RQ-6. Control effectiveness

The system shall represent the effectiveness of relevant security controls.

Control effectiveness shall be capable of reducing adjusted incident probability or otherwise reducing modeled risk.

The MVP shall use a documented, bounded effectiveness score. Where configuration strength, incident history, or compliance telemetry are simulated, they must be identified as simulated inputs.

## RQ-7. Financial impact

The system shall estimate financial impact for an asset/risk scenario.

Financial impact shall support the PRD's business-impact concepts, including where applicable:

- downtime cost
- breach cost
- regulatory penalty
- reputational impact

Organization-specific financial inputs shall be accepted where available. The UI and API shall distinguish supplied inputs from assumptions or simulated values.

## RQ-8. Incident probability

The system shall calculate an adjusted incident probability from the modeled vulnerability, asset, threat/exposure, and control inputs.

The calculation must be bounded and deterministic for identical inputs in the MVP.

The system shall retain enough intermediate values to explain how the probability was produced.

## RQ-9. Expected Annual Loss

The primary MVP financial-risk metric shall be Expected Annual Loss (EAL).

For a modeled asset/risk scenario:

**EAL = Financial Impact × Adjusted Incident Probability**

Where probability represents the modeled annual probability of the incident.

The implementation shall expose the input impact, adjusted probability, and resulting EAL so the number is auditable.

Example acceptance test:

> Given an asset with financial impact X and adjusted incident probability Y, the system calculates EAL = X × Y.

## RQ-10. Enterprise-level aggregation

The system shall aggregate asset-level EAL into an enterprise-level financial exposure.

For the MVP, enterprise EAL shall be calculated from the supported asset/risk records using a documented aggregation rule.

The enterprise result shall be reproducible from the underlying asset-level values and shall not be hardcoded in the dashboard.

## RQ-11. Asset-level aggregation

The system shall calculate and expose EAL for each asset.

An asset detail view shall show:

- asset criticality
- relevant vulnerabilities
- severity/exposure inputs
- control effectiveness
- financial impact
- adjusted incident probability
- EAL
- key contributing factors

The technical drill-down shall allow an analyst to trace an asset's financial risk back to its source inputs.

---

# AI Decision Support

## AI-1. Recommendations

The system shall generate prioritized mitigation recommendations based on the highest-impact modeled risks.

Recommendations may include the PRD's examples such as:

- patching
- access tightening
- segmentation
- monitoring

Each recommendation shall include:

- affected asset/risk
- proposed action
- estimated cost where available
- estimated risk reduction
- rationale
- relevant inputs/assumptions

Recommendations are advisory only; the MVP shall not execute remediation.

## AI-2. Risk explanations

The system shall explain why a risk is high and which inputs contribute to it.

For a displayed risk figure or recommendation, the explanation shall identify the relevant asset, vulnerability/severity, exposure/threat factors, controls, financial impact, probability, and resulting risk where applicable.

AI-generated explanations must remain traceable to underlying data/model rationale.

## AI-3. Natural-language queries

The MVP shall provide a natural-language risk-query interface.

At minimum, it shall support the PRD example:

> “What is our highest financial cyber risk today?”

The response shall be grounded in current backend risk data and identify the relevant risk contributor(s), rather than returning a generic cybersecurity answer.

If an external LLM is unavailable, the application shall provide a deterministic fallback for supported MVP queries.

## AI-4. Scenario analysis

The system shall support what-if analysis for changes to modeled controls, vulnerabilities, probability, cost, or timing.

At minimum, the scenario engine shall support examples aligned with the PRD, such as:

- enforcing MFA for privileged accounts
- delaying remediation for a defined period

A scenario shall show baseline versus simulated results, including the change in risk/EAL where the available model supports it.

Scenario simulation shall not mutate the baseline dataset unless explicitly requested by the application workflow.

---

# Investment Optimization

## IO-1. Budget input

The system shall accept a cybersecurity investment budget.

Budget values shall be represented in INR for the MVP while keeping currency configurable as specified by the PRD.

Input validation shall reject invalid or negative budgets.

## IO-2. Remediation actions

The system shall represent candidate remediation/control initiatives.

Each initiative shall identify:

- action/control
- affected risk/assets
- implementation cost
- expected risk reduction
- rationale
- applicable framework mapping when available

The candidate set may be synthetic for the MVP.

## IO-3. Cost

Each candidate investment shall have a numeric cost in the configured currency.

The optimizer shall use the same cost value displayed to the user.

## IO-4. Expected risk reduction

Each candidate investment shall have an estimated reduction in modeled risk/EAL.

The estimate shall be explicit and traceable to the assumptions or modeled changes used to produce it.

## IO-5. Risk-reduction-per-cost

The system shall calculate:

**Risk Reduction per Cost = Expected Risk Reduction / Investment Cost**

This metric shall be available for candidate initiatives and shall support prioritization.

Zero-cost initiatives shall be handled explicitly rather than producing an invalid division.

## IO-6. Recommended investment portfolio

Given a fixed budget, the optimizer shall recommend a portfolio of candidate initiatives that maximizes modeled risk reduction without exceeding the budget.

A simple greedy or knapsack-style approach is sufficient for the MVP.

The result shall show:

- selected initiatives
- total cost
- total expected risk reduction
- remaining budget
- baseline risk
- modeled residual risk

The optimizer shall not imply that the recommendation is an actuarially guaranteed outcome.

## IO-7. ROSI

The system shall calculate Return on Security Investment (ROSI) for individual initiatives and/or the recommended portfolio.

The exact formula used shall be documented by the implementation and consistently applied.

ROSI shall be based on modeled financial risk reduction and investment cost, with assumptions clearly displayed.

## IO-8. Investment vs. risk-reduction visualization

The dashboard shall visualize investment spend against modeled risk reduction.

The visualization shall make it possible to identify:

- low-cost/high-impact opportunities
- diminishing returns where represented by the optimization model
- the recommended budget allocation
- baseline versus post-investment modeled risk

---

# Dashboard

## D-1. Enterprise Risk Score

The executive dashboard shall display an Enterprise Risk Score derived from backend risk data.

The score shall not be hardcoded and shall have a documented relationship to the underlying risk model.

## D-2. Financial Exposure

The dashboard shall display total modeled financial exposure for the enterprise.

The figure shall be traceable to the enterprise aggregation of underlying risk records.

## D-3. EAL

The dashboard shall display enterprise EAL and allow navigation to the asset/risk records contributing to it.

## D-4. Risk trends

The dashboard shall show risk trends using available historical/simulated snapshots.

If no historical data exists, the UI shall clearly indicate that trend data is unavailable rather than inventing history.

## D-5. Top contributors

The dashboard shall rank the largest contributors to enterprise risk using calculated backend values.

Contributors should be drillable to their underlying assets/vulnerabilities.

## D-6. Critical assets

The dashboard shall identify assets with the highest criticality and/or materially significant modeled financial risk.

## D-7. Critical vulnerabilities

The dashboard shall identify vulnerabilities that materially contribute to modeled risk, considering severity and affected asset context.

## D-8. Recommendations

The executive dashboard shall surface prioritized risk-reduction opportunities.

Each recommendation shall link to its rationale and, where available, its estimated cost and risk reduction.

## D-9. Drill-down

The technical view shall support drill-down from enterprise risk to:

1. business/unit or grouping where available
2. asset
3. vulnerability/finding
4. control
5. calculation inputs and modeled result

The drill-down shall preserve traceability between displayed aggregate values and source records.

---

# Compliance

## C-1. NIST CSF MVP priority

The MVP shall prioritize NIST Cybersecurity Framework (NIST CSF) mapping.

Findings, controls, or recommendations shall be mappable to relevant NIST CSF functions/categories/subcategories where the MVP dataset provides sufficient mapping information.

## C-2. Modular framework architecture

Framework mapping shall be implemented behind a framework-independent interface/rules layer.

The architecture shall allow additional mappings to be added without rewriting the risk engine, optimizer, dashboard, or core data model.

The planned extension targets are:

- ISO/IEC 27001
- CIS Controls
- RBI CSF
- SEBI CSCRF

These additional mappings are architectural extension points for the MVP rather than mandatory complete implementations unless separately enabled.

## C-3. Evidence-based reporting

The system shall support generation of a compliance-oriented report from the mapped findings/controls and their available evidence.

The MVP report shall avoid claiming compliance merely because a mapping exists; it should identify the mapped control/finding and available evidence/status.

---

# Cross-Cutting MVP Requirements

## Explainability and traceability

Every displayed financial risk number and recommendation shall be traceable to:

- source input data
- calculation
- assumptions
- model rationale
- confidence/limitations where appropriate

The UI shall distinguish simulated/demo values from measured organizational data.

## Data validation

Inputs shall be validated for required fields, numeric ranges, probability bounds, severity/criticality values, and budget/cost constraints.

Invalid inputs shall produce understandable errors.

## Data freshness

The architecture shall support refreshed calculations after new input data is loaded. The PRD targets near-real-time processing for the broader product; the hackathon MVP may demonstrate refresh through simulated ingestion rather than production streaming.

## Interoperability boundary

The MVP shall use a normalized internal data model so future REST, syslog, and STIX/TAXII integrations can be added without coupling the risk engine to a specific vendor.

## Security and access

The production PRD calls for encryption, RBAC, and audit logging. The hackathon MVP should keep these as architecture considerations and avoid introducing production-scale infrastructure that is not required for the demonstration.

---

# Acceptance Criteria

## Risk Quantification

### Asset inventory
- **Given** a valid asset dataset, **when** it is loaded, **then** each asset receives a unique identifier and the required inventory fields are available to the risk engine.
- **Given** two assets with different criticality values but otherwise identical risk inputs, **when** risk is calculated, **then** the criticality factor affects their modeled risk according to the documented formula.

### Vulnerability data
- **Given** a vulnerability finding linked to an existing asset, **when** the finding is ingested, **then** it is normalized and associated with that asset.
- **Given** an invalid asset reference, **when** a vulnerability is loaded, **then** validation reports the invalid relationship rather than silently attaching it to another asset.

### Severity
- **Given** a vulnerability severity value, **when** normalization runs, **then** the system stores the normalized severity used by the risk engine and preserves the source value where available.

### Threat/exposure
- **Given** the same vulnerability under different exposure/threat inputs, **when** risk is recalculated, **then** adjusted incident probability changes according to the documented factor weights.

### Control effectiveness
- **Given** identical asset and vulnerability inputs with different control-effectiveness scores, **when** risk is calculated, **then** the stronger modeled control reduces risk according to the documented calculation.

### Financial impact
- **Given** valid downtime, breach, penalty, and/or reputational impact inputs, **when** financial impact is calculated, **then** the result is reproducible and the contributing inputs are displayed.

### Incident probability
- **Given** valid risk factors, **when** adjusted probability is calculated, **then** it remains within the configured probability bounds and the intermediate factors are available for explanation.

### EAL
- **Given** an asset with financial impact X and adjusted incident probability Y, **when** EAL is calculated, **then** EAL equals X × Y.
- **Given** identical inputs, **when** EAL is calculated twice, **then** the result is identical.

### Enterprise aggregation
- **Given** asset-level EAL values, **when** enterprise aggregation runs, **then** the enterprise value equals the documented aggregation of those asset-level values.
- **Given** a change to one asset's underlying risk input, **when** the model refreshes, **then** the affected asset and enterprise values update.

### Asset-level aggregation
- **Given** an asset with linked vulnerabilities and controls, **when** its detail view is opened, **then** the user can see the inputs and calculated EAL contributing to that asset's risk.

## AI Decision Support

### Recommendations
- **Given** material risk contributors, **when** recommendations are generated, **then** the output contains prioritized actions with rationale and modeled risk-reduction estimates where available.
- **Given** a recommendation, **when** its explanation is opened, **then** it identifies the underlying risk factors used to generate it.

### Risk explanations
- **Given** a displayed EAL or risk score, **when** the user requests an explanation, **then** the system identifies the major contributing inputs and calculation path.

### Natural-language query
- **Given** the supported query “What is our highest financial cyber risk today?”, **when** the query is submitted, **then** the response identifies the highest-ranked current financial risk from backend data and provides supporting context.
- **Given** the LLM is unavailable, **when** the supported query is submitted, **then** the deterministic fallback returns a valid data-grounded response.

### Scenario analysis
- **Given** a baseline scenario and a valid what-if change, **when** simulation runs, **then** the system displays baseline and simulated risk/EAL and the difference between them.
- **Given** a scenario simulation, **when** the user exits without applying it, **then** baseline data remains unchanged.

## Investment Optimization

### Budget
- **Given** a positive budget in INR, **when** optimization starts, **then** the optimizer uses that value as the spending constraint.
- **Given** a negative or invalid budget, **when** it is submitted, **then** validation prevents optimization and explains the error.

### Remediation actions
- **Given** candidate actions with cost and expected risk reduction, **when** they are loaded, **then** each is available to the optimizer with its affected risk context.

### Risk reduction per cost
- **Given** an initiative with cost C > 0 and expected risk reduction R, **when** the ratio is calculated, **then** risk-reduction-per-cost equals R / C.

### Portfolio
- **Given** candidate initiatives and budget B, **when** optimization completes, **then** total selected cost is ≤ B.
- **Given** the same deterministic candidate set and budget, **when** optimization runs repeatedly, **then** it produces the same portfolio.
- **Given** the selected portfolio, **when** results are displayed, **then** total cost, expected risk reduction, remaining budget, and residual modeled risk are shown.

### ROSI
- **Given** an initiative with a modeled financial risk reduction and investment cost, **when** ROSI is calculated, **then** the documented ROSI formula is applied consistently and its inputs are visible.

### Investment visualization
- **Given** multiple candidate investments, **when** the investment analysis view opens, **then** the user can compare spend with modeled risk reduction and identify the recommended allocation.

## Dashboard

- **Given** current backend risk data, **when** the executive dashboard loads, **then** Enterprise Risk Score, Financial Exposure, and EAL are calculated from backend data rather than hardcoded.
- **Given** multiple risk contributors, **when** the dashboard loads, **then** contributors are ranked by their calculated contribution.
- **Given** critical assets or vulnerabilities, **when** the dashboard loads, **then** they are surfaced according to the documented ranking logic.
- **Given** historical snapshots, **when** the trend view loads, **then** the trend reflects those snapshots.
- **Given** no historical snapshots, **when** the trend view loads, **then** the UI indicates that trend data is unavailable.
- **Given** a dashboard contributor, **when** the user drills down, **then** the corresponding underlying asset/finding and calculation inputs can be inspected.

## Compliance

- **Given** a finding/control with a defined NIST CSF mapping, **when** the compliance view loads, **then** the mapping is displayed.
- **Given** a mapped item without supporting evidence, **when** a compliance report is generated, **then** the report does not represent the mapping alone as proof of compliance.
- **Given** a future framework mapping module, **when** it is added, **then** the core risk and dashboard components do not need framework-specific rewrites.

---

# MVP Definition of Done

The MVP is complete when a demonstrable end-to-end flow works:

1. Load simulated assets and vulnerabilities.
2. Calculate explainable asset-level risk and EAL.
3. Aggregate risk to the enterprise.
4. Display Enterprise Risk Score, Financial Exposure, EAL, and top contributors.
5. Drill from an enterprise contributor to an asset and its risk inputs.
6. Generate at least one data-grounded natural-language risk answer.
7. Generate prioritized remediation recommendations.
8. Run a what-if scenario and show baseline versus simulated risk.
9. Accept a budget and recommend a risk-reducing investment portfolio.
10. Show cost, modeled risk reduction, risk-reduction-per-cost, and ROSI.
11. Visualize investment versus risk reduction.
12. Demonstrate NIST CSF mapping.
13. Keep simulated/demo data clearly labeled.
14. Ensure every financial risk number can be traced to its inputs, calculation, and assumptions.
