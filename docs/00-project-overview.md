# CyberQuant AI --- Project Overview

## 1. Project Name

**CyberQuant AI**

CyberQuant AI is an AI-powered continuous cyber risk quantification and
security investment optimization platform for the SIH26105 problem
statement.

## 2. SIH Problem Statement

**SIH26105 --- AI-Powered Continuous Cyber Risk Quantification and
Investment Optimization Platform**

The platform addresses the gap between technical cybersecurity findings
and financially meaningful business risk. It is intended to continuously
transform security telemetry, asset context, vulnerabilities, and
control effectiveness into understandable financial exposure and
actionable investment decisions.

## 3. Problem

Organizations commonly express cyber risk using qualitative labels such
as **Low / Medium / High**. These ratings are difficult to compare,
become stale when assessments are periodic, and do not clearly connect
technical findings to business or financial consequences.

Organizations therefore struggle to:

-   **Quantify cyber risk financially** --- translate technical risk
    into metrics such as Expected Annual Loss (EAL) and financial
    exposure.
-   **Prioritize vulnerabilities** --- distinguish vulnerabilities on
    business-critical assets from technically severe but lower-impact
    findings.
-   **Understand business impact** --- connect assets, service
    dependencies, downtime, breach costs, regulatory penalties, and
    reputational impact to cyber events.
-   **Optimize security spending** --- determine which controls or
    mitigations provide the greatest risk reduction for a constrained
    budget.
-   **Communicate cyber risk to executives** --- give CISOs, CFOs,
    boards, regulators, and auditors defensible numbers and clear
    explanations rather than technical findings alone.

The core gap is that cybersecurity data is rich in technical detail but
is not consistently converted into a continuous, explainable
business-risk model.

## 4. Solution

**CyberQuant AI** provides a unified platform that converts
cybersecurity telemetry and business context into financial risk
measurements and investment recommendations.

The platform:

1.  **Ingests security/IT information** from simulated or connected
    sources such as asset inventories, vulnerability scanners, SIEM,
    EDR, IAM, CSPM, and threat intelligence.
2.  **Normalizes asset and vulnerability information** into a common
    data model so heterogeneous findings can be analyzed consistently.
3.  **Evaluates asset criticality** using business importance and
    service/dependency context.
4.  **Evaluates security control effectiveness** using available
    configuration, incident, compliance, and telemetry signals.
5.  **Estimates incident likelihood** using statistical/ML-based risk
    modeling and available threat/vulnerability/control signals.
6.  **Estimates financial impact** including factors such as downtime,
    breach costs, regulatory penalties, and reputational impact.
7.  **Calculates Expected Annual Loss (EAL)** and financial exposure at
    asset, business-unit, and enterprise levels.
8.  **Identifies top risk contributors** so users can see which assets,
    vulnerabilities, controls, or risk factors drive the largest portion
    of financial exposure.
9.  **Recommends mitigations** such as patching, access tightening,
    segmentation, or monitoring, with estimated risk-reduction impact.
10. **Optimizes investments under a budget** by selecting
    controls/initiatives that maximize risk reduction subject to the
    available budget.
11. **Supports what-if simulations** to estimate the effect of actions
    such as enforcing MFA or delaying remediation.
12. **Provides natural-language risk queries** so users can ask
    questions such as, "What is our highest financial cyber risk today?"
13. **Maps selected controls to cybersecurity frameworks**, with the MVP
    demonstrating NIST CSF mapping and the broader PRD targeting ISO/IEC
    27001, NIST CSF, CIS Controls, RBI CSF, and SEBI CSCRF.

The high-level product flow is:

**Security/IT data → normalization → asset/control context → likelihood
& impact → financial risk → prioritization → mitigation → investment
optimization → scenario analysis → executive decision support**

## 5. Target Users

  -----------------------------------------------------------------------
  User                                Primary Need
  ----------------------------------- -----------------------------------
  **CISO / Security Leader**          Enterprise risk view, top financial
                                      risk contributors, defensible
                                      numbers for leadership and the
                                      board

  **Risk & Compliance Officer**       Framework-mapped evidence, risk
                                      assessments, audit/regulatory
                                      support

  **CFO / Board Member**              Financial exposure, EAL, ROSI, and
                                      evidence for security investment
                                      decisions

  **Security Analyst / Engineer**     Asset/control-level drill-down,
                                      prioritized findings, remediation
                                      backlog, actionable recommendations

  **Regulator / Auditor**             Framework mapping, evidence, and
                                      historical risk/compliance
                                      information
  -----------------------------------------------------------------------

## 6. Core Value Proposition

> **"Turn cyber risk into business language and turn security spend into
> an optimization problem."**

CyberQuant AI translates technical cybersecurity signals into financial
exposure and then uses those measurements to help decision-makers
allocate security budgets where they produce the greatest measurable
risk reduction.

## 7. MVP

The hackathon MVP must demonstrate a complete end-to-end decision
workflow rather than attempting the full enterprise platform.

### MVP capabilities

-   **Simulated data from 2--3 sources**, such as:
    -   asset inventory
    -   vulnerability findings
    -   mock SIEM/security telemetry
-   **Asset inventory** with business-criticality information.
-   **Vulnerability findings** associated with assets and their risk
    characteristics.
-   **EAL calculation** at asset and enterprise level using a defined,
    explainable statistical model.
-   **Enterprise financial exposure** showing the monetary impact of
    cyber risk.
-   **Top risk contributors** identifying the assets/findings
    contributing most to financial exposure.
-   **Simple budget optimization** that recommends controls/mitigations
    under a fixed budget, using risk-reduction/cost effectiveness.
-   **ROSI (Return on Security Investment)** and cost-benefit
    calculations for recommended initiatives.
-   **Executive dashboard** containing at minimum:
    -   enterprise risk score
    -   total financial exposure
    -   top risk contributors
    -   risk-reduction opportunities
    -   relevant risk trend information where available
-   **One working natural-language query**, for example:
    -   "What is our highest financial cyber risk today?"
-   **NIST CSF mapping** to demonstrate framework/control mapping.
-   **Scenario simulation** showing how a proposed action changes risk
    and financial exposure.

### MVP demo outcome

A successful demo should allow a judge to start with simulated
enterprise data, identify the largest financial cyber risk, inspect its
technical causes, select mitigations, provide a budget, see an optimized
investment plan and ROSI, run a what-if scenario, and observe the
resulting reduction in financial exposure.

## 8. Non-Goals

The MVP is **not** intended to:

-   Replace SIEM, EDR, vulnerability scanners, CSPM, IAM, or other
    existing security tools.
-   Automatically remediate production systems, patch assets, or change
    production configurations.
-   Make legal, insurance underwriting, actuarial, or regulatory
    decisions on behalf of qualified professionals.
-   Provide full enterprise integrations with every security/IT
    platform.
-   Implement production-grade high-volume real-time streaming
    infrastructure.

The platform should **ingest and analyze** information from security
systems rather than attempt to become those systems.

## 9. Core User Journey

The primary demo/user journey is:

**Login / Demo** → **Executive Dashboard** → **Identify top financial
risk** → **Drill into asset** → **Inspect vulnerabilities and
contributing factors** → **View recommended mitigations** → **Enter
security budget** → **Optimize investment** → **Review ROSI and expected
risk reduction** → **Run scenario simulation** → **Observe reduced
financial exposure** → **Ask an AI risk question**

At every important step, the system should make the connection between
technical evidence, financial impact, and business decision clear.

## 10. Important Product Principles

### Explainability

Every important risk figure and AI-generated recommendation should be
traceable to the underlying data, assumptions, and model rationale.
Avoid presenting false precision.

### Financial Quantification

Risk should ultimately be expressed in financially meaningful terms such
as **EAL, financial exposure, risk reduction, cost, and ROSI**, while
retaining the technical evidence behind those numbers.

### Business Context

Technical severity alone must not determine priority. Asset criticality,
business importance, service dependencies, and estimated financial
impact must influence risk.

### Risk Prioritization

The product should surface the risks that matter most to the
organization rather than simply listing the largest number of technical
findings.

### Cost Effectiveness

Security recommendations should consider both expected risk reduction
and implementation cost. Budget optimization should help answer **where
the next rupee should be spent**.

### Human-in-the-Loop

AI recommendations support decision-making; they do not replace
responsible security, financial, compliance, or executive approval.

### Clear Separation Between Simulated Data and Real Telemetry

The MVP uses simulated/sample data where appropriate. The UI, APIs, data
models, and documentation must clearly distinguish simulated demo values
from real enterprise telemetry. Never imply that generated sample data
represents an actual organization's security state.

------------------------------------------------------------------------

## Implementation Guidance for AI Coding Agents

When building CyberQuant AI, treat this document as the product-level
orientation and the SIH26105 PRD as the authoritative requirements
source.

Prioritize the **hackathon MVP and end-to-end demo path** before
implementing enterprise-scale capabilities. Keep risk calculations
deterministic and explainable where possible, expose assumptions used in
financial models, and design components so simulated data sources can
later be replaced by real connectors.

The MVP architecture should conceptually separate:

1.  **Data ingestion**
2.  **Normalization**
3.  **Asset/business context**
4.  **Risk quantification**
5.  **Mitigation/recommendation**
6.  **Investment optimization**
7.  **Scenario simulation**
8.  **Framework mapping**
9.  **Natural-language decision support**
10. **Executive and technical presentation**

Do not build features merely because they are technically interesting.
Every MVP feature should contribute to the core story:

**technical evidence → financial risk → prioritized action → optimized
security investment → measurable risk reduction.**
