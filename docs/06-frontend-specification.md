# CyberQuant AI --- Frontend Specification

> **Status:** Authoritative frontend specification for the hackathon
> MVP\
> **Technology:** React, Vite, TypeScript, Tailwind CSS, Recharts,
> Axios, Lucide React\
> **Design goal:** Professional enterprise cybersecurity risk platform
>
> Business metrics, risk values, financial exposure, and other dynamic
> data **must come from APIs**. Do not hardcode business metrics in
> frontend components.

------------------------------------------------------------------------

## 1. Frontend Goals

The CyberQuant AI frontend provides a single interface for turning
technical cybersecurity findings into:

-   financial risk visibility
-   prioritized vulnerabilities
-   mitigation recommendations
-   security investment decisions
-   scenario analysis
-   compliance visibility
-   natural-language risk analysis

The primary UX story is:

**Dashboard → identify financial risk → investigate asset/risk → choose
mitigation → optimize investment → simulate outcome → ask AI**

The interface should feel suitable for an enterprise CISO/security
operations environment rather than a consumer dashboard.

------------------------------------------------------------------------

## 2. Technology Stack

  Technology         Purpose
  ------------------ --------------------------------------------
  **React**          Component-based UI
  **Vite**           Frontend build/development tooling
  **TypeScript**     Type safety
  **Tailwind CSS**   Styling and responsive layout
  **Recharts**       Risk, trend, and investment visualizations
  **Axios**          API communication
  **Lucide React**   Consistent iconography

Use TypeScript throughout the frontend. Avoid `any` unless there is a
documented integration reason.

------------------------------------------------------------------------

## 3. Application Layout

Use a persistent enterprise application shell.

### Desktop

``` text
┌────────────────────────────────────────────────────────────────────┐
│ CyberQuant AI                         Data: SIMULATED   Last Updated │
├───────────────┬────────────────────────────────────────────────────┤
│               │                                                    │
│ Dashboard     │                                                    │
│ Assets        │                 Page Content                       │
│ Risk Analysis │                                                    │
│ Investments   │                                                    │
│ Scenarios     │                                                    │
│ Compliance    │                                                    │
│ AI Assistant  │                                                    │
│               │                                                    │
│ Settings      │                                                    │
└───────────────┴────────────────────────────────────────────────────┘
```

### Application shell requirements

-   Left navigation on desktop.
-   Collapsible/mobile navigation on smaller screens.
-   Top bar containing:
    -   page title/breadcrumb
    -   simulated/live data indicator
    -   last-updated timestamp
    -   optional refresh action
    -   user/profile control
-   Main content area should support scrolling independently from
    navigation.
-   Avoid excessive gradients, decorative animations, or visual noise.
-   Use restrained cybersecurity/enterprise visual language.

------------------------------------------------------------------------

# 4. Pages

## 4.1 Executive Dashboard

### Purpose

Give executives an immediate answer to:

> **"How much cyber risk do we currently carry, where is it
> concentrated, and where should we spend to reduce it?"**

### KPI cards

Display:

1.  **Enterprise Risk Score**
    -   0--100 normalized score.
    -   Show risk level:
        -   Low
        -   Moderate
        -   High
        -   Critical
2.  **Total Financial Exposure**
    -   Enterprise exposure in INR.
    -   Use the canonical enterprise aggregation from the risk engine.
3.  **Expected Annual Loss**
    -   Enterprise EAL in INR.
4.  **Critical Assets**
    -   Count of assets classified as critical.
5.  **Critical Vulnerabilities**
    -   Count of critical vulnerabilities.
6.  **Risk Trend**
    -   Show recent risk-score/EAL movement.
    -   Use API-provided historical data.

Each card should support a tooltip explaining the metric.

### Main dashboard sections

#### Risk trend

Use a Recharts line/area visualization showing:

-   time
-   enterprise risk score and/or EAL
-   selected time range where supported

Do not fabricate historical values.

If the API has no historical data, show an informative empty state
instead of inventing a trend.

#### Top Financial Risk Contributors

Ranked table/list containing:

-   asset
-   business unit
-   risk level
-   financial exposure/EAL
-   primary risk driver
-   vulnerability count

Allow clicking a contributor to open the asset/risk detail view.

#### Risk Reduction Opportunities

Show recommended actions with:

-   mitigation/control
-   affected assets
-   estimated cost
-   expected risk reduction
-   ROSI where available
-   priority

### Dashboard metadata

Display:

-   **Last Updated:** API timestamp.
-   **Data Status:** `SIMULATED` or `LIVE`.

The simulated/live indicator must be visually obvious but not alarming.

------------------------------------------------------------------------

# 5. Assets Page

## Purpose

Provide technical/business context behind enterprise financial risk.

### Asset table

Columns:

  Column                Description
  --------------------- -----------------------------------------------
  Asset                 Asset/service name
  Type                  Server, application, database, endpoint, etc.
  Business Unit         Owning business unit
  Criticality           1--5
  Financial Value       INR
  Risk Exposure         INR / EAL
  Vulnerability Count   Number of findings

### Table requirements

-   Sortable columns where meaningful.
-   Search/filter controls.
-   Severity/criticality indicators.
-   Pagination if API supports it.
-   Keyboard-accessible rows.
-   Responsive behavior.
-   Empty state when no assets exist.
-   Loading skeleton while fetching.
-   Error state with retry.

### Asset detail

Clicking an asset opens a detail page or drawer containing:

-   asset name
-   type
-   business unit
-   criticality
-   financial value
-   downtime cost
-   data sensitivity
-   internet exposure
-   control effectiveness
-   total EAL
-   vulnerability count
-   associated vulnerabilities
-   major risk drivers
-   recommended mitigations

The asset detail view must link to the corresponding risk analysis.

------------------------------------------------------------------------

# 6. Risk Analysis Page

## Purpose

Explain why an asset/finding is risky and quantify its financial
consequence.

### Risk findings table

Show:

-   vulnerability/finding
-   affected asset
-   CVSS
-   probability
-   financial impact
-   EAL
-   severity
-   major risk driver

### Example table

``` text
Finding          Asset        CVSS   Probability   Impact       EAL       Severity
CVE-XXXX         Payment DB   9.8    36%           ₹10.0L       ₹3.6L     Critical
CVE-YYYY         API Server   8.1    21%           ₹6.0L        ₹1.26L    High
```

Values must be API-driven.

### Filters

Support filtering by:

-   severity
-   asset
-   business unit
-   CVSS range
-   risk level
-   EAL range

### Risk detail

Selecting a finding should show:

-   finding details
-   affected asset
-   CVSS
-   normalized factors
-   incident probability
-   financial impact components
-   EAL
-   control effectiveness
-   confidence/data completeness
-   major risk drivers
-   recommended mitigations

------------------------------------------------------------------------

## 6.1 Explainability Panel

Every risk result should have an accessible explainability panel.

Show:

### Inputs

-   CVSS
-   asset criticality
-   internet exposure
-   exploitability
-   threat activity
-   data sensitivity
-   control effectiveness
-   financial-impact inputs

### Intermediate calculations

Display the major stages:

``` text
CVSS
  ↓
Base Probability
  ↓
Risk Adjustment Factors
  ↓
Pre-Control Probability
  ↓
Control Effectiveness
  ↓
Incident Probability
  ↓
Financial Impact
  ↓
EAL
```

### Explanation

Use plain business language.

Example:

> **CVSS 9.8, internet exposure HIGH, asset criticality 5/5, and low
> control effectiveness increased the estimated incident probability.**

Also show:

-   assumptions
-   confidence/data completeness
-   simulated-data warning where applicable

The frontend must not reproduce or independently calculate the
risk-engine formula. The backend risk engine is the source of truth.

------------------------------------------------------------------------

# 7. Investment Optimizer

## Purpose

Answer:

> **"Given this budget, which security investments produce the greatest
> risk reduction?"**

### Inputs

Provide:

-   **Budget**
-   Currency: INR

Validate:

-   required
-   numeric
-   non-negative

### Recommended controls table

Show:

  Control                         Cost   Risk Reduction   ROSI Priority
  ----------------------------- ------ ---------------- ------ ----------
  MFA for privileged accounts      API              API    API API
  Network segmentation             API              API    API API
  Critical patching                API              API    API API

Do not calculate recommendation values in the frontend.

### Summary

Show:

-   total recommended spend
-   remaining budget
-   estimated total risk reduction
-   estimated resulting EAL
-   average/aggregate ROSI where supplied by API

### Investment vs Risk Reduction Chart

Use Recharts.

Recommended visualization:

-   X-axis: investment/spend in INR
-   Y-axis: expected risk reduction in INR or percentage, matching the
    API response
-   Highlight recommended/optimal spend point
-   Tooltip with:
    -   investment
    -   risk reduction
    -   resulting EAL
    -   ROSI

If the API does not provide a curve, do not manufacture one from
hardcoded values.

------------------------------------------------------------------------

# 8. Scenario Simulator

## Purpose

Allow users to ask:

> **"What happens to our financial exposure if we apply these
> mitigations?"**

### Scenario controls

Allow users to select one or more mitigations, such as:

-   improve control effectiveness
-   remediate vulnerability
-   reduce internet exposure
-   apply recommended control

The available mitigation list should come from the API.

### Results

Show four prominent metrics:

1.  **Before Exposure**
2.  **After Exposure**
3.  **Absolute Reduction**
4.  **Percentage Reduction**

Example:

``` text
Before Exposure       ₹25.0L
After Exposure        ₹14.0L
Absolute Reduction    ₹11.0L
Percentage Reduction  44%
```

### Scenario comparison

Use a simple before/after visualization.

Also show:

-   affected assets
-   affected vulnerabilities
-   controls changed
-   assumptions
-   scenario timestamp

### Important rule

Scenario calculations must be performed by the risk engine/API using the
canonical risk pipeline. The frontend only sends scenario changes and
renders returned results.

------------------------------------------------------------------------

# 9. Compliance Page

## Purpose

Provide an understandable view of how modeled security controls map to
cybersecurity frameworks.

### MVP framework

The hackathon MVP must demonstrate:

**NIST CSF**

### Table

Show:

  NIST CSF Control   Description   Mapping Status                Evidence
  ------------------ ------------- ----------------------------- ----------
  Control ID         API           Mapped / Partial / Unmapped   API

### Features

-   Search controls.
-   Filter by mapping status.
-   Show mapped assets/findings where available.
-   Show evidence/details in a drawer or detail panel.
-   Clear distinction between:
    -   Mapped
    -   Partially mapped
    -   Unmapped

The broader product may later support:

-   ISO/IEC 27001
-   CIS Controls
-   RBI CSF
-   SEBI CSCRF

Do not implement unsupported framework data as if it were available.

------------------------------------------------------------------------

# 10. AI Assistant

## Purpose

Provide a natural-language interface to CyberQuant AI's risk data.

### Chat UI

Use:

-   message history
-   user messages
-   assistant responses
-   input box
-   send button
-   loading/typing state
-   error state
-   clear conversation action if supported

### Example questions

Support questions such as:

> "What is our highest financial cyber risk?"

> "Which vulnerabilities contribute most to expected losses?"

> "What should we fix first?"

### Response design

AI responses should be concise and business-oriented.

Where supported, responses should include:

-   metric values
-   referenced assets/findings
-   recommended actions
-   assumptions
-   links/actions to relevant dashboard pages

### Suggested question chips

Provide quick-start prompts such as:

-   Highest financial risk?
-   Biggest EAL contributor?
-   What should we fix first?
-   Best use of our budget?

Suggested prompts are UI helpers; actual answers must come from the
API/AI service.

### Loading state

While waiting for the AI API:

-   disable duplicate submission
-   show an assistant loading indicator
-   retain the user's submitted question

### Error state

If the AI service fails:

> "The AI risk assistant is temporarily unavailable. Please try again."

Do not display raw stack traces or backend internals.

------------------------------------------------------------------------

# 11. API Integration

Use **Axios** through a centralized API client.

Recommended pattern:

``` text
src/
└── services/
    ├── apiClient.ts
    ├── dashboardApi.ts
    ├── assetsApi.ts
    ├── riskApi.ts
    ├── investmentApi.ts
    ├── scenarioApi.ts
    ├── complianceApi.ts
    └── assistantApi.ts
```

### API client responsibilities

`apiClient.ts` should centralize:

-   base URL
-   timeout
-   common headers
-   authentication handling when introduced
-   response/error handling
-   request interceptors where necessary

### Page/service separation

React components should not contain raw Axios calls.

Preferred flow:

``` text
Page
 ↓
Hook / query state
 ↓
Service
 ↓
Axios API client
 ↓
Backend
```

This keeps UI components modular and testable.

------------------------------------------------------------------------

# 12. TypeScript Data Models

Create shared API/domain types.

Recommended examples:

``` text
EnterpriseMetrics
Asset
Vulnerability
RiskResult
RiskExplanation
FinancialImpact
RiskContributor
RiskReductionOpportunity
InvestmentRecommendation
Scenario
ScenarioResult
ComplianceControl
ChatMessage
ApiError
```

Types should represent API contracts rather than duplicating business
logic.

Example conceptual model:

``` ts
type RiskLevel = "LOW" | "MODERATE" | "HIGH" | "CRITICAL";

interface RiskResult {
  id: string;
  assetId: string;
  cvss: number;
  incidentProbability: number;
  financialImpact: number | null;
  eal: number | null;
  riskLevel: RiskLevel;
  confidence: number;
  majorRiskDrivers: string[];
}
```

Exact fields should match the backend API contract.

------------------------------------------------------------------------

# 13. Recommended Frontend Folder Structure

``` text
src/
├── app/
│   ├── App.tsx
│   ├── routes.tsx
│   └── providers/
│
├── assets/
│   └── ...
│
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Badge.tsx
│   │   ├── Tooltip.tsx
│   │   ├── Modal.tsx
│   │   ├── Drawer.tsx
│   │   ├── Skeleton.tsx
│   │   └── EmptyState.tsx
│   │
│   ├── layout/
│   │   ├── AppShell.tsx
│   │   ├── Sidebar.tsx
│   │   ├── TopBar.tsx
│   │   └── MobileNav.tsx
│   │
│   ├── dashboard/
│   │   ├── MetricCard.tsx
│   │   ├── RiskTrendChart.tsx
│   │   ├── TopRiskContributors.tsx
│   │   └── RiskReductionOpportunities.tsx
│   │
│   ├── assets/
│   │   ├── AssetTable.tsx
│   │   ├── AssetFilters.tsx
│   │   └── AssetDetail.tsx
│   │
│   ├── risk/
│   │   ├── RiskTable.tsx
│   │   ├── RiskFilters.tsx
│   │   ├── RiskDetail.tsx
│   │   └── ExplainabilityPanel.tsx
│   │
│   ├── investment/
│   │   ├── BudgetInput.tsx
│   │   ├── RecommendationTable.tsx
│   │   ├── InvestmentSummary.tsx
│   │   └── InvestmentRiskChart.tsx
│   │
│   ├── scenario/
│   │   ├── MitigationSelector.tsx
│   │   ├── ScenarioSummary.tsx
│   │   └── ScenarioComparisonChart.tsx
│   │
│   ├── compliance/
│   │   ├── ComplianceTable.tsx
│   │   ├── ComplianceFilters.tsx
│   │   └── ControlDetail.tsx
│   │
│   └── assistant/
│       ├── ChatWindow.tsx
│       ├── ChatMessage.tsx
│       ├── ChatInput.tsx
│       └── SuggestedQuestions.tsx
│
├── pages/
│   ├── DashboardPage.tsx
│   ├── AssetsPage.tsx
│   ├── AssetDetailPage.tsx
│   ├── RiskAnalysisPage.tsx
│   ├── InvestmentOptimizerPage.tsx
│   ├── ScenarioSimulatorPage.tsx
│   ├── CompliancePage.tsx
│   └── AssistantPage.tsx
│
├── services/
│   ├── apiClient.ts
│   ├── dashboardApi.ts
│   ├── assetsApi.ts
│   ├── riskApi.ts
│   ├── investmentApi.ts
│   ├── scenarioApi.ts
│   ├── complianceApi.ts
│   └── assistantApi.ts
│
├── hooks/
│   ├── useDashboard.ts
│   ├── useAssets.ts
│   ├── useRiskAnalysis.ts
│   ├── useInvestmentOptimizer.ts
│   ├── useScenario.ts
│   ├── useCompliance.ts
│   └── useAssistant.ts
│
├── types/
│   ├── api.ts
│   ├── risk.ts
│   ├── asset.ts
│   ├── investment.ts
│   ├── scenario.ts
│   └── compliance.ts
│
├── utils/
│   ├── currency.ts
│   ├── dates.ts
│   ├── severity.ts
│   └── formatting.ts
│
├── config/
│   └── environment.ts
│
├── main.tsx
└── index.css
```

Components should have a single clear responsibility. Avoid creating one
giant dashboard component containing all application logic.

------------------------------------------------------------------------

# 14. UX States

Every API-backed view must account for four states:

## Loading

Use skeletons/placeholders rather than leaving large blank regions.

Examples:

-   KPI card skeleton
-   table row skeleton
-   chart skeleton
-   assistant loading indicator

Avoid excessive spinner usage.

## Empty

Explain why there is no data and what the user can do.

Example:

> **No risk contributors found**\
> There are currently no risk contributors returned for this assessment.

Do not display fake data as a fallback.

## Error

Show:

-   concise human-readable message
-   retry action where appropriate

Example:

> **Unable to load enterprise metrics**\
> We couldn't retrieve the latest risk data.\
> **Retry**

Never expose raw backend errors, stack traces, or internal URLs.

## Success

Show data with:

-   clear hierarchy
-   appropriate units
-   timestamps
-   data-source state where relevant

------------------------------------------------------------------------

# 15. Responsive Design

The frontend must work across:

-   desktop
-   laptop
-   tablet
-   mobile

### Desktop

Use the full sidebar and multi-column dashboard cards.

### Tablet

-   Collapse some multi-column sections.
-   Preserve readable tables.
-   Allow horizontal table scrolling where necessary.

### Mobile

-   Replace persistent sidebar with a menu/drawer.
-   Stack KPI cards.
-   Stack chart sections.
-   Make tables horizontally scrollable or provide mobile-friendly card
    representations.
-   Keep important actions reachable.
-   Do not shrink text to the point of unreadability.

------------------------------------------------------------------------

# 16. Accessibility

Use accessible HTML and interaction patterns.

### Requirements

-   Semantic headings.
-   Semantic table elements.
-   Labels for all form inputs.
-   Keyboard-accessible controls.
-   Visible focus states.
-   Buttons must have accessible names.
-   Charts should have supporting textual summaries where necessary.
-   Do not rely on color alone to communicate severity.
-   Dialogs/drawers must support keyboard navigation and proper focus
    management.
-   Sufficient contrast between text and background.

### Tables

Accessible tables must include:

-   table caption or accessible label
-   column headers
-   meaningful row/column relationships
-   keyboard-accessible interactive rows/actions

------------------------------------------------------------------------

# 17. Severity and Risk Indicators

Use consistent risk levels throughout the application:

-   **Low**
-   **Moderate**
-   **High**
-   **Critical**

Severity should be communicated through a combination of:

-   label
-   icon where useful
-   restrained visual treatment

Do not rely only on red/yellow/green color.

Use the backend/API risk level as the source of truth.

------------------------------------------------------------------------

# 18. Currency and Number Formatting

CyberQuant AI's default MVP currency is **INR**.

Use consistent INR formatting throughout:

``` text
₹10,00,000
₹2,50,000
₹1.25 Cr
```

The exact compact notation can be standardized by the frontend utility
layer, but full values should remain available through
tooltips/accessibility labels.

Create a reusable formatter:

``` text
utils/currency.ts
```

Never concatenate currency strings manually throughout components.

Probability and percentage values should also use consistent formatting.

Examples:

``` text
36%
44.2%
0.36
```

Choose one display convention per context and keep it consistent.

------------------------------------------------------------------------

# 19. Tooltips

Use tooltips for metrics that may not be obvious to executives.

Important tooltip candidates:

-   Enterprise Risk Score
-   EAL
-   Financial Exposure
-   ROSI
-   Confidence
-   Risk Reduction
-   Control Effectiveness

Example:

> **Expected Annual Loss**\
> Estimated annualized financial loss based on the modeled incident
> probability and financial impact. It is not a guaranteed loss.

Tooltips should supplement, not replace, visible labels.

------------------------------------------------------------------------

# 20. Data Status

The frontend must clearly distinguish simulated and live data.

Display a persistent indicator such as:

``` text
● SIMULATED DATA
```

or:

``` text
● LIVE DATA
```

The value must come from application/API configuration or metadata, not
from a hardcoded assumption inside each page.

For MVP demo data, clearly communicate that financial and security
values are simulated.

------------------------------------------------------------------------

# 21. No Hardcoded Business Metrics

The following must **never** be hardcoded in React components:

-   enterprise risk score
-   EAL
-   financial exposure
-   asset counts
-   vulnerability counts
-   risk trends
-   asset financial values
-   probabilities
-   investment recommendations
-   risk reduction
-   ROSI
-   scenario results
-   compliance status
-   AI answers

Static UI copy, labels, icons, risk-level names, and layout
configuration may be defined in frontend code.

Business metrics must come from API responses.

------------------------------------------------------------------------

# 22. Frontend Risk Calculation Boundary

The frontend is a **presentation and interaction layer**.

It must not independently implement the authoritative risk formula.

For example, do not calculate:

``` text
EAL = probability × financial impact
```

inside a React component if the backend already provides EAL.

The backend risk engine is the source of truth.

The frontend may calculate purely presentational values where necessary,
such as:

-   table pagination state
-   chart dimensions
-   display formatting
-   local UI percentages when explicitly defined by the API contract

Any business/risk calculation must be implemented in the
backend/risk-engine layer and returned through the API.

------------------------------------------------------------------------

# 23. Navigation

Recommended navigation:

``` text
Dashboard
Assets
Risk Analysis
Investment Optimizer
Scenario Simulator
Compliance
AI Assistant
```

Optional later sections:

``` text
Reports
Settings
Administration
```

For the hackathon MVP, prioritize the seven core areas above.

------------------------------------------------------------------------

# 24. Visual Design Direction

The visual language should communicate:

**trust + security + financial intelligence + enterprise software**

Recommended characteristics:

-   dark or light enterprise theme with strong contrast
-   restrained accent color
-   clean cards
-   subtle borders
-   compact but readable tables
-   clear typography hierarchy
-   consistent spacing
-   minimal decorative elements
-   data-first layouts
-   professional chart styling

Avoid:

-   excessive neon/cyberpunk styling
-   animated backgrounds
-   unnecessary 3D effects
-   dense walls of text
-   dashboard widgets with no decision value
-   decorative charts with no API-backed data

The interface should look credible to a CISO, CFO, auditor, or
enterprise security team.

------------------------------------------------------------------------

# 25. Component Design Principles

### Reusable primitives

Build common components first:

-   Card
-   Badge
-   Button
-   Input
-   Select
-   Tooltip
-   Modal
-   Drawer
-   Table
-   Skeleton
-   EmptyState
-   ErrorState

### Domain components

Build reusable domain components:

-   MetricCard
-   RiskBadge
-   CurrencyValue
-   RiskTrendChart
-   ExplainabilityPanel
-   InvestmentRecommendationTable
-   ScenarioComparison
-   ComplianceStatusBadge

### Page components

Pages should compose domain components rather than contain all rendering
logic themselves.

Preferred:

``` text
DashboardPage
 ├── MetricCard[]
 ├── RiskTrendChart
 ├── TopRiskContributors
 └── RiskReductionOpportunities
```

Avoid:

``` text
DashboardPage.tsx
 ├── API calls
 ├── risk calculations
 ├── formatting
 ├── chart configuration
 ├── table implementation
 └── every dashboard component
```

------------------------------------------------------------------------

# 26. Error Handling

Axios/API errors should be normalized by the service layer.

The UI should distinguish:

-   network failure
-   authentication/authorization failure
-   validation error
-   not found
-   server error
-   AI service failure

Use human-readable messages.

Never expose:

-   stack traces
-   database errors
-   internal service names
-   secrets
-   raw exception payloads

------------------------------------------------------------------------

# 27. Environment Configuration

API endpoints must be environment-configurable.

Recommended Vite variables:

``` text
VITE_API_BASE_URL
```

Do not hardcode deployment-specific backend URLs into components.

Use an environment/config layer so development, demo, and deployment
environments can point to different APIs.

------------------------------------------------------------------------

# 28. Hackathon MVP Priority

Implement in this order:

1.  **Application shell/navigation**
2.  **Executive Dashboard**
3.  **Assets + asset detail**
4.  **Risk Analysis + Explainability**
5.  **Investment Optimizer**
6.  **Scenario Simulator**
7.  **NIST CSF Compliance**
8.  **AI Assistant**
9.  **Responsive/accessibility refinement**
10. **Loading/empty/error states**

The critical end-to-end demo must work before secondary polish.

------------------------------------------------------------------------

# 29. Definition of Done

The frontend MVP is complete when a user can:

1.  Open CyberQuant AI.
2.  See whether data is simulated or live.
3.  View enterprise risk metrics retrieved from the API.
4.  Identify top financial risk contributors.
5.  Open an asset and inspect its context.
6.  Inspect vulnerabilities and EAL.
7.  Understand the major risk drivers through the explainability panel.
8.  Enter a security budget.
9.  View API-generated investment recommendations and ROSI.
10. View investment-vs-risk-reduction information.
11. Select mitigations in the scenario simulator.
12. See before/after financial exposure and reduction.
13. Inspect NIST CSF mappings.
14. Ask a natural-language risk question.
15. Receive an API-backed AI response.
16. Experience appropriate loading, empty, and error states.
17. Use the application on desktop and mobile.

------------------------------------------------------------------------

## 30. Source-of-Truth Rules for AI Coding Agents

When implementing this frontend:

1.  **Do not hardcode business metrics.**
2.  **Do not reimplement the backend risk formulas in the frontend.**
3.  Treat API contracts as the source of dynamic data.
4.  Keep components modular and single-purpose.
5.  Keep API access inside service modules/hooks rather than UI
    components.
6.  Use TypeScript types for API/domain data.
7.  Clearly distinguish simulated data from live telemetry.
8.  Preserve explainability information returned by the risk engine.
9.  Use INR consistently for MVP financial values.
10. Do not invent historical trends, risk values, recommendations,
    compliance mappings, or AI responses when APIs return no data.
11. Every major API-backed page must implement loading, empty, error,
    and success states.
12. Follow the authoritative risk-engine specification in
    `docs/04-risk-engine.md` for risk terminology and calculations.
13. Optimize for the hackathon's end-to-end demo path before adding
    non-MVP functionality.

**The frontend should make the core CyberQuant AI story immediately
understandable:**

> **Technical evidence → financial risk → prioritized action → optimized
> investment → measurable risk reduction.**
