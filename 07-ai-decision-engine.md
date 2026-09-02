# CyberQuant AI --- AI Decision Engine Specification

> **Status:** Authoritative specification for the AI decision-support
> layer\
> **Scope:** Hackathon MVP with deterministic fallback\
> **Primary principle:** The AI layer must explain and reason over
> existing structured risk data; it must not invent cybersecurity or
> financial facts.
>
> The MVP **must work without an external LLM**. An external LLM may be
> added later behind the same service interface.

------------------------------------------------------------------------

## 1. Purpose

The AI Decision Engine is the decision-support layer of CyberQuant AI.

Its purpose is to turn existing, calculated risk information into
concise business-language answers and prioritized actions.

The AI layer sits **above** the authoritative risk engine:

``` text
Security / IT Data
        ↓
Normalization
        ↓
Risk Engine
        ↓
Structured Risk Data
        ↓
AI Decision Engine
        ↓
Answer + Evidence + Drivers + Recommendation
```

The AI layer must **not become a second risk engine**.

Risk calculations such as incident probability, financial impact, EAL,
enterprise exposure, and enterprise risk score must come from the
canonical backend risk engine and its APIs.

------------------------------------------------------------------------

# 2. Core Principles

The AI decision engine follows these principles:

### 2.1 Grounded in backend data

Every factual claim about the organization's risk must be supported by
structured backend data.

### 2.2 Deterministic MVP

The MVP must produce reproducible answers for the same:

-   input question
-   backend dataset
-   engine configuration
-   application state

### 2.3 No invented facts

The AI must never invent:

-   CVEs
-   vulnerabilities
-   assets
-   financial losses
-   probabilities
-   EAL values
-   compliance status
-   security controls
-   threat activity
-   remediation costs
-   historical incidents

If the required information is unavailable, the response must say so.

### 2.4 Explainable

Responses should identify the evidence and risk drivers used to reach
the conclusion.

### 2.5 Estimates are estimates

Calculated risk values must be described as modeled estimates, not
guaranteed outcomes.

### 2.6 Human-in-the-loop

Recommendations support human decision-making. They do not automatically
remediate systems or guarantee a security outcome.

------------------------------------------------------------------------

# 3. Capabilities

## 3.1 Natural Language Query

The engine must support natural-language questions over the structured
CyberQuant AI dataset.

Initial supported questions include:

-   **"What is our highest financial cyber risk?"**
-   **"Which vulnerability contributes most to expected loss?"**
-   **"Which asset is most exposed?"**
-   **"What should we fix first?"**
-   **"How much risk can we reduce with ₹10 lakh?"**

The MVP should also tolerate reasonable variations of these questions.

Examples:

``` text
What is our biggest cyber risk?
Which vulnerability has the highest EAL?
Which asset has the highest exposure?
What should we prioritize?
What can we achieve with a 10 lakh budget?
```

Natural-language interpretation should map the question to a known
structured operation rather than asking a language model to calculate
arbitrary business metrics.

------------------------------------------------------------------------

# 4. Query Intent Model

The MVP should classify incoming questions into deterministic intents.

Recommended intents:

``` text
HIGHEST_FINANCIAL_RISK
TOP_VULNERABILITY
MOST_EXPOSED_ASSET
RECOMMENDED_PRIORITY
BUDGET_RISK_REDUCTION
RISK_EXPLANATION
SCENARIO_INTERPRETATION
UNSUPPORTED
```

### Example mapping

  -----------------------------------------------------------------------
  User question                       Intent
  ----------------------------------- -----------------------------------
  "What is our highest financial      `HIGHEST_FINANCIAL_RISK`
  cyber risk?"                        

  "Which vulnerability contributes    `TOP_VULNERABILITY`
  most to expected loss?"             

  "Which asset is most exposed?"      `MOST_EXPOSED_ASSET`

  "What should we fix first?"         `RECOMMENDED_PRIORITY`

  "How much risk can we reduce with   `BUDGET_RISK_REDUCTION`
  ₹10 lakh?"                          

  "Why is the payment database high   `RISK_EXPLANATION`
  risk?"                              

  "What happens if we enable MFA?"    `SCENARIO_INTERPRETATION`
  -----------------------------------------------------------------------

For the MVP, intent classification may use deterministic keyword/phrase
matching and simple parsing.

------------------------------------------------------------------------

# 5. Natural Language Query Processing

Recommended pipeline:

``` text
User Question
     ↓
Normalize text
     ↓
Detect intent
     ↓
Extract entities/parameters
     ↓
Retrieve structured backend data
     ↓
Apply deterministic decision logic
     ↓
Generate grounded response
     ↓
Validate response against source data
     ↓
Return structured AI response
```

### Important rule

The AI must **retrieve first and answer second**.

It must not answer from assumptions when structured data is available.

------------------------------------------------------------------------

# 6. Backend Data Contract

The AI service should consume structured data rather than scrape or
infer values from dashboard text.

Recommended data categories:

### Enterprise

-   enterprise risk score
-   enterprise risk level
-   total financial exposure
-   enterprise EAL
-   last updated
-   data status (`SIMULATED` / `LIVE`)

### Assets

-   asset ID
-   asset name
-   asset type
-   business unit
-   criticality
-   financial value
-   downtime cost
-   exposure
-   EAL
-   vulnerability count

### Vulnerabilities

-   finding ID
-   vulnerability/CVE identifier when actually present
-   affected asset
-   CVSS
-   incident probability
-   financial impact
-   EAL
-   severity
-   exploitability
-   threat activity
-   control effectiveness
-   major risk drivers

### Investments

-   control/mitigation ID
-   control name
-   affected assets
-   remediation cost
-   estimated risk reduction
-   ROSI
-   resulting EAL where provided
-   priority

### Scenarios

-   baseline exposure
-   scenario exposure
-   absolute reduction
-   percentage reduction
-   selected mitigations
-   changed assumptions

### Compliance

-   framework
-   control ID
-   mapping status
-   evidence

The AI must only reference fields actually returned by the backend.

------------------------------------------------------------------------

# 7. Risk Explanation

The AI should explain **existing calculated risk data**.

It must not recalculate risk using a separate AI formula.

For example, when asked:

> "Why is this asset high risk?"

The service should retrieve the asset's structured risk result and
explain:

-   CVSS
-   asset criticality
-   internet exposure
-   exploitability
-   threat activity
-   data sensitivity
-   control effectiveness
-   incident probability
-   financial impact
-   EAL
-   confidence/data completeness

### Example

> **Answer:** The Payment Database is currently one of the highest
> financial cyber risks.
>
> **Key evidence:** Its modeled EAL is ₹3.6 lakh, based on an estimated
> incident probability of 36% and financial impact of ₹10 lakh.
>
> **Risk drivers:** CVSS 9.8, HIGH internet exposure, 5/5 asset
> criticality, and low control effectiveness.
>
> **Recommendation:** Prioritize the associated critical vulnerability
> and the recommended control improvement.
>
> **Estimated impact:** The backend model estimates that the proposed
> mitigation could reduce EAL by the returned risk-reduction amount.
>
> **Limitations:** These are modeled estimates based on the available
> data. The MVP dataset is simulated.

Numbers in the response must exactly match the structured source data.

------------------------------------------------------------------------

# 8. Recommendations

Recommendations should be prioritized using backend-provided
information.

Primary factors:

1.  **EAL**
2.  **Severity**
3.  **Asset criticality**
4.  **Control effectiveness**
5.  **Remediation cost**
6.  **Estimated risk reduction**

The recommendation layer must not invent a remediation cost or
risk-reduction value.

## 8.1 MVP prioritization logic

For a simple deterministic fallback, sort candidate remediation actions
using:

1.  Higher EAL contribution first.
2.  Higher severity next.
3.  Higher asset criticality next.
4.  Lower control effectiveness next.
5.  Higher estimated risk reduction next.
6.  Lower remediation cost as a tie-breaker.

This ordering is a **decision-prioritization rule**, not a replacement
for the authoritative risk calculation.

If the backend already returns an authoritative recommendation/priority,
use that instead of recreating the ranking.

## 8.2 Recommendation language

Use cautious language:

Good:

> "This is the highest-priority remediation based on the current modeled
> EAL and asset criticality."

Avoid:

> "This fix will eliminate the risk."

Good:

> "The scenario model estimates a ₹X reduction in EAL."

Avoid:

> "This fix will save the organization ₹X."

The former describes a model result; the latter incorrectly presents an
estimate as a guaranteed outcome.

------------------------------------------------------------------------

# 9. Budget Questions

For:

> "How much risk can we reduce with ₹10 lakh?"

the AI should:

1.  Extract the budget: `₹10,00,000`.
2.  Send/use the budget with the investment optimization API.
3.  Retrieve recommended controls.
4.  Retrieve total estimated risk reduction.
5.  Retrieve remaining budget and resulting EAL where available.
6.  Explain the result.

Example response:

> **Answer:** With a ₹10 lakh budget, the optimizer recommends the
> returned set of controls.
>
> **Key evidence:** The selected initiatives cost ₹X and have an
> estimated combined risk reduction of ₹Y.
>
> **Risk drivers:** The recommendations target the highest-value risk
> contributors within the budget constraint.
>
> **Recommendation:** Prioritize the optimizer's recommended control
> set.
>
> **Estimated impact:** The modeled enterprise EAL changes from ₹A to
> ₹B.
>
> **Limitations:** Results depend on the assumptions and simulated data
> currently used by the risk model.

If the optimization API does not return enough information to answer the
question, say that the available data is insufficient.

------------------------------------------------------------------------

# 10. Scenario Interpretation

The AI should translate scenario outputs into business language.

Scenario input may include changes to:

-   control effectiveness
-   vulnerability status
-   exposure
-   remediation status
-   selected mitigations

The scenario engine returns the authoritative result.

The AI explains:

``` text
Before Exposure
       ↓
Scenario Change
       ↓
After Exposure
       ↓
Absolute Reduction
       ↓
Percentage Reduction
```

Example:

> **Answer:** The selected MFA mitigation reduces the modeled enterprise
> exposure from ₹25 lakh to ₹14 lakh.
>
> **Key evidence:** The scenario reports an estimated reduction of ₹11
> lakh, or 44%.
>
> **Risk drivers:** The change primarily affects the risk associated
> with the targeted privileged-access exposure.
>
> **Recommendation:** Consider the mitigation if the implementation cost
> and operational impact are acceptable.
>
> **Estimated impact:** ₹11 lakh modeled exposure reduction.
>
> **Limitations:** This is a scenario estimate, not a guarantee that
> actual losses will decrease by ₹11 lakh.

------------------------------------------------------------------------

# 11. External LLM Architecture

The architecture must allow an external LLM to be added without making
the MVP dependent on it.

Recommended abstraction:

``` text
                    ┌─────────────────────┐
                    │  AI Decision API    │
                    └──────────┬──────────┘
                               │
                     ┌─────────▼─────────┐
                     │ Intent / Query    │
                     │ Orchestrator      │
                     └─────────┬─────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
       ┌─────────▼──────────┐      ┌────────▼─────────┐
       │ Deterministic      │      │ External LLM     │
       │ Decision Provider  │      │ Provider         │
       └─────────┬──────────┘      └────────┬─────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               ↓
                     Structured Response
```

Recommended interface:

``` ts
interface AIDecisionProvider {
  answer(
    question: string,
    context: RiskContext
  ): Promise<AIDecisionResponse>;
}
```

Implement at least:

``` text
DeterministicDecisionProvider
```

Later:

``` text
LLMDecisionProvider
```

The rest of the application should depend on the interface, not directly
on a specific LLM vendor.

------------------------------------------------------------------------

# 12. MVP Deterministic Fallback

The MVP fallback should be completely functional without an external
model.

### Step 1 --- Normalize

Normalize:

-   lowercase/uppercase differences
-   whitespace
-   punctuation
-   INR budget expressions

### Step 2 --- Detect intent

Match known question patterns.

### Step 3 --- Retrieve data

Fetch only the structured data required for the intent.

### Step 4 --- Apply deterministic logic

Examples:

``` text
highest financial risk
→ select risk item with maximum EAL

highest EAL vulnerability
→ select vulnerability with maximum EAL

most exposed asset
→ select asset with maximum exposure/EAL according to API semantics

what should we fix first
→ use backend recommendations or deterministic priority ordering

budget question
→ call investment optimizer with extracted budget
```

### Step 5 --- Generate response

Populate the standard response structure.

### Step 6 --- Validate

Before returning:

-   every number must exist in source data
-   every referenced entity must exist
-   no unsupported claim should be present
-   simulated/live status must be preserved

------------------------------------------------------------------------

# 13. Response Format

All AI responses should follow a consistent structure.

## Required sections

### Answer

Direct answer to the user's question.

### Key Evidence

Relevant structured metrics supporting the answer.

### Risk Drivers

The main factors contributing to the result.

### Recommendation

Action supported by the current risk/investment data.

### Estimated Impact

Modeled risk reduction, EAL, exposure, or other relevant impact.

### Confidence / Limitations

Include when appropriate, especially when:

-   data is incomplete
-   financial inputs are missing
-   confidence is low
-   data is simulated
-   the answer depends on scenario assumptions

------------------------------------------------------------------------

# 14. Structured AI Response

The API should preferably return structured data alongside rendered
text.

Recommended model:

``` ts
interface AIDecisionResponse {
  answer: string;
  keyEvidence: EvidenceItem[];
  riskDrivers: string[];
  recommendation: string | null;
  estimatedImpact: ImpactSummary | null;
  confidence: number | null;
  limitations: string[];
  dataStatus: "SIMULATED" | "LIVE";
  sourceIds: string[];
}
```

Example:

``` json
{
  "answer": "The Payment Database is currently the highest financial cyber risk.",
  "keyEvidence": [
    {
      "label": "EAL",
      "value": "₹3,60,000",
      "sourceId": "risk-123"
    },
    {
      "label": "Incident Probability",
      "value": "36%",
      "sourceId": "risk-123"
    }
  ],
  "riskDrivers": [
    "CVSS 9.8",
    "HIGH internet exposure",
    "Asset criticality 5/5",
    "Low control effectiveness"
  ],
  "recommendation": "Prioritize the associated critical vulnerability and recommended control.",
  "estimatedImpact": null,
  "confidence": 89,
  "limitations": [
    "Risk values are modeled estimates.",
    "Demo data is simulated."
  ],
  "dataStatus": "SIMULATED",
  "sourceIds": ["risk-123"]
}
```

The frontend can render this structure consistently without parsing
arbitrary prose.

------------------------------------------------------------------------

# 15. Grounding and Evidence

Every factual metric in an AI response should have a source in the
retrieved structured context.

Recommended source identifiers:

``` text
asset:<asset-id>
risk:<risk-id>
vulnerability:<finding-id>
investment:<initiative-id>
scenario:<scenario-id>
compliance:<control-id>
enterprise:<assessment-id>
```

The system should retain these IDs internally even if the user sees
friendly names.

This makes responses auditable and helps prevent hallucinations.

------------------------------------------------------------------------

# 16. Guardrails

## 16.1 Estimates vs facts

The AI must distinguish:

**Fact from source data:**

> "The API reports CVSS 9.8."

**Modeled estimate:**

> "The risk model estimates a 36% incident probability."

Never blur these categories.

------------------------------------------------------------------------

## 16.2 Synthetic data

If:

``` text
dataStatus = SIMULATED
```

the response should explicitly communicate that relevant results are
based on simulated/demo data.

Never say:

> "Your organization experienced..."

when the underlying data is simulated.

Prefer:

> "The simulated dataset indicates..."

------------------------------------------------------------------------

## 16.3 CVEs

Never invent a CVE.

Only mention a CVE identifier if it exists in the backend data.

If no identifier is available:

> "the critical vulnerability affecting the payment database"

rather than generating an identifier.

------------------------------------------------------------------------

## 16.4 Financial losses

Never invent:

-   breach costs
-   downtime costs
-   regulatory costs
-   recovery costs
-   reputation costs
-   EAL
-   financial exposure

If unavailable:

> "Financial impact is unavailable because the required financial inputs
> are missing."

------------------------------------------------------------------------

## 16.5 Compliance

Never invent compliance status.

Only state:

-   Mapped
-   Partially mapped
-   Unmapped

when that status is supplied by the compliance service.

------------------------------------------------------------------------

## 16.6 Recommendations

Recommendations are not guarantees.

Avoid:

> "This control will prevent a breach."

Prefer:

> "The model estimates that this control would reduce the modeled risk."

------------------------------------------------------------------------

## 16.7 Missing information

When required data is unavailable, the AI should say:

> "I don't have enough structured data to answer that reliably."

Then identify the missing information when useful.

Do not fill the gap using general assumptions.

------------------------------------------------------------------------

# 17. Unsupported Questions

If a question is outside the supported risk dataset:

> **Answer:** I can answer questions about CyberQuant AI's modeled cyber
> risk, financial exposure, vulnerabilities, assets, investments,
> scenarios, and compliance mappings. I don't have enough structured
> data to answer that question reliably.

The system must not use general cybersecurity knowledge to fabricate
organization-specific facts.

------------------------------------------------------------------------

# 18. Confidence and Limitations

Use the risk engine's confidence/data-completeness value where
available.

The AI should not invent a separate model-accuracy percentage.

Example:

> **Confidence:** 78% data completeness.
>
> **Limitations:** Financial inputs for one impact component are
> unavailable, so the modeled EAL should be interpreted cautiously.

If confidence is unavailable:

> "Confidence information is not available for this result."

If the dataset is simulated, mention that separately.

------------------------------------------------------------------------

# 19. Response Examples

## 19.1 Highest financial risk

**Question:**

> What is our highest financial cyber risk?

**Expected response shape:**

> **Answer:** The Payment Database is currently the highest financial
> cyber risk based on the available modeled risk data.
>
> **Key evidence:** It has the highest returned EAL of ₹X.
>
> **Risk drivers:** CVSS X, asset criticality X/5, HIGH exposure, and
> low control effectiveness.
>
> **Recommendation:** Prioritize the associated remediation/control
> improvement.
>
> **Estimated impact:** The selected mitigation has an estimated EAL
> reduction of ₹Y, according to the current model.
>
> **Limitations:** Results are modeled estimates and may use simulated
> data.

------------------------------------------------------------------------

## 19.2 Highest EAL vulnerability

**Question:**

> Which vulnerability contributes most to expected loss?

The engine should:

1.  Retrieve vulnerability risk results.
2.  Select the highest EAL vulnerability.
3.  Return the exact vulnerability and asset names from source data.
4.  Explain its major risk drivers.

Never create a vulnerability identifier that does not exist.

------------------------------------------------------------------------

## 19.3 Most exposed asset

**Question:**

> Which asset is most exposed?

The answer must clarify what "exposed" means in the returned data.

For example:

> "The API identifies the Payment Database as the highest financial
> exposure asset, with modeled EAL of ₹X."

Do not automatically equate "internet exposure" with "financial
exposure" unless the user asks specifically about network exposure.

------------------------------------------------------------------------

## 19.4 What should we fix first?

The engine should use backend recommendations where available.

Response:

> **Answer:** The first priority is the remediation returned by the
> optimizer/risk recommendation service.
>
> **Key evidence:** It affects an asset with criticality X/5 and
> contributes ₹Y of modeled EAL.
>
> **Risk drivers:** CVSS X, exposure X, and control effectiveness X%.
>
> **Recommendation:** Prioritize this action subject to operational
> feasibility and approval.
>
> **Estimated impact:** The backend estimates ₹Z of risk reduction.

------------------------------------------------------------------------

## 19.5 Budget optimization

**Question:**

> How much risk can we reduce with ₹10 lakh?

The engine must pass the parsed budget to the investment optimizer.

Response should report:

-   recommended controls
-   total cost
-   estimated risk reduction
-   resulting EAL if available
-   remaining budget
-   ROSI if available

No investment value should be invented.

------------------------------------------------------------------------

# 20. Security and Privacy

The AI service handles potentially sensitive security information.

It should:

-   minimize data sent to an external LLM
-   send only the context required for the question
-   avoid sending secrets or credentials
-   avoid exposing raw internal infrastructure details unnecessarily
-   preserve access-control boundaries
-   log decision metadata without unnecessarily logging sensitive user
    content

When an external LLM is introduced, the integration must explicitly
define:

-   what data is sent
-   where it is processed
-   retention behavior
-   authentication
-   failure behavior
-   access control

The hackathon MVP should remain fully functional without external data
transmission.

------------------------------------------------------------------------

# 21. Failure Handling

### Backend unavailable

Return:

> "I can't retrieve the current risk data right now. Please try again."

Do not answer from stale assumptions unless cached data is explicitly
marked and supported.

### Empty dataset

Return:

> "There is currently no risk data available for this assessment."

Do not fabricate an answer.

### Missing financial data

Return a useful partial answer when possible:

> "The vulnerability has the highest modeled incident probability, but I
> cannot determine its financial EAL because financial-impact data is
> incomplete."

### Unsupported intent

Return the supported-capability message described above.

### External LLM unavailable

Automatically fall back to the deterministic provider if the fallback
has sufficient structured data.

The MVP must not fail merely because an external LLM is unavailable.

------------------------------------------------------------------------

# 22. Testing Requirements

The AI decision engine must include deterministic tests.

## Query tests

Test at least:

``` text
"What is our highest financial cyber risk?"
"Which vulnerability contributes most to expected loss?"
"Which asset is most exposed?"
"What should we fix first?"
"How much risk can we reduce with ₹10 lakh?"
```

Each test should verify:

-   correct intent
-   correct source entity
-   correct metrics
-   no invented values
-   correct simulated/live status

## Guardrail tests

Verify that the engine:

-   never invents CVEs
-   never invents financial values
-   never invents compliance status
-   never describes simulated data as real
-   preserves model-estimate language
-   reports missing information
-   does not produce unsupported recommendations

## Determinism tests

Given the same:

-   question
-   structured context
-   configuration

the deterministic provider must return the same result.

------------------------------------------------------------------------

# 23. Recommended Service Structure

``` text
backend/
└── ai/
    ├── __init__
    ├── interfaces/
    │   └── decision_provider.py
    │
    ├── providers/
    │   ├── deterministic_provider.py
    │   └── llm_provider.py
    │
    ├── intent/
    │   ├── classifier.py
    │   └── intents.py
    │
    ├── retrieval/
    │   └── risk_context.py
    │
    ├── recommendations/
    │   └── prioritizer.py
    │
    ├── prompts/
    │   └── ...
    │
    ├── guardrails/
    │   └── validator.py
    │
    └── schemas/
        └── responses.py
```

Equivalent structure may be used in another backend language, but the
separation of responsibilities should remain.

------------------------------------------------------------------------

# 24. External LLM Provider Contract

When an LLM is introduced, it must receive **grounded context** rather
than being allowed to answer from unconstrained knowledge.

Recommended flow:

``` text
Question
   ↓
Intent detection
   ↓
Backend retrieval
   ↓
Structured risk context
   ↓
LLM
   ↓
Structured response
   ↓
Grounding validation
   ↓
User
```

The LLM should primarily perform:

-   natural-language understanding
-   summarization
-   explanation
-   response composition

It should not be the authoritative calculator for:

-   EAL
-   probability
-   financial impact
-   enterprise exposure
-   investment optimization
-   scenario results

Those remain backend responsibilities.

------------------------------------------------------------------------

# 25. Definition of Done

The AI Decision Engine MVP is complete when:

1.  Natural-language risk questions can be answered without an external
    LLM.
2.  Questions are mapped to deterministic supported intents.
3.  Answers use backend structured data.
4.  Risk explanations reference actual calculated values.
5.  Recommendations are based on EAL, severity, criticality, control
    effectiveness, cost, and/or returned risk reduction.
6.  Budget questions invoke the investment optimizer.
7.  Scenario results can be translated into business language.
8.  Every response follows the standard answer structure.
9.  Simulated data is clearly identified.
10. Missing information is explicitly reported.
11. CVEs, financial values, compliance status, and other facts are never
    fabricated.
12. The architecture supports a future external LLM provider.
13. External LLM failure does not break the MVP when deterministic
    fallback data is available.
14. Deterministic tests verify grounding and guardrails.

------------------------------------------------------------------------

# 26. Source-of-Truth Rules for AI Coding Agents

1.  **The risk engine is the source of truth for calculated risk.**
2.  **The backend data/API is the source of truth for
    organization-specific facts.**
3.  The AI layer explains and orchestrates; it does not invent.
4.  Never calculate a competing EAL/probability model inside the AI
    layer.
5.  Never fabricate missing cybersecurity or financial information.
6.  Never present simulated data as real telemetry.
7.  Always distinguish facts from modeled estimates.
8.  Recommendations must be traceable to structured evidence.
9.  Scenario interpretations must use returned scenario results.
10. External LLM integration must remain optional.
11. The deterministic provider must remain usable as the hackathon MVP
    fallback.
12. Every AI response should expose enough evidence and limitations for
    a user to understand why the answer was produced.

**Core AI principle:**

> **Retrieve → reason over structured evidence → explain → recommend
> cautiously. Never invent.**
