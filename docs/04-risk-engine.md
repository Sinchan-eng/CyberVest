# CyberQuant AI --- Risk Engine Specification

> **Status:** Authoritative specification\
> **Scope:** Hackathon MVP\
> **Principles:** Deterministic, transparent, explainable, bounded, and
> testable
>
> This document is the **source of truth for all CyberQuant AI risk
> calculations**. Implementations must use the definitions and formulas
> below unless this document is explicitly revised.

------------------------------------------------------------------------

## 1. Risk Calculation Pipeline

The risk engine follows this deterministic pipeline:

**Technical findings → asset context → threat/exposure factors → control
effectiveness → incident probability → financial impact → Expected
Annual Loss → enterprise aggregation**

For each vulnerability/finding:

1.  Read the technical finding, primarily its CVSS score and
    exploitability/threat information.
2.  Attach asset context such as criticality, financial value, data
    sensitivity, and downtime cost.
3.  Convert exposure, exploitability, and threat activity into bounded
    adjustment factors.
4.  Apply the asset's security-control effectiveness.
5.  Calculate the estimated annual incident probability.
6.  Calculate the financial impact if the incident occurs.
7.  Calculate **EAL = incident probability × financial impact**.
8.  Aggregate asset-level EALs to obtain enterprise exposure.

All intermediate values must be retained so the result can be explained.

------------------------------------------------------------------------

## 2. Input Variables

  -------------------------------------------------------------------------
  Variable                MVP definition          Normalization
  ----------------------- ----------------------- -------------------------
  **CVSS score**          Vulnerability severity  `cvss / 10`
                          from 0.0--10.0          

  **Asset criticality**   Business criticality    `(criticality - 1) / 4`
                          rating from 1--5        

  **Financial value**     Monetary value          INR; used as supplied
                          associated with the     
                          asset/business service  

  **Downtime cost**       Estimated cost of one   INR
                          incident's downtime     

  **Internet exposure**   Exposure level: LOW,    LOW=0.0, MEDIUM=0.5,
                          MEDIUM, HIGH            HIGH=1.0

  **Data sensitivity**    Data sensitivity: LOW,  LOW=0.0, MEDIUM=0.5,
                          MEDIUM, HIGH            HIGH=1.0

  **Exploitability**      Exploitability level or 0.0--1.0
                          normalized              
                          exploitability input    

  **Threat activity**     Current threat activity LOW=0.0, MEDIUM=0.5,
                          level                   HIGH=1.0

  **Control               Estimated effectiveness 0.0--1.0
  effectiveness**         of relevant             
                          preventive/detective    
                          controls                
  -------------------------------------------------------------------------

### Input bounds

The engine must clamp normalized inputs to **\[0, 1\]**.

-   CVSS must be clamped to `[0, 10]` before normalization.
-   Criticality must be clamped to `[1, 5]` before normalization.
-   Exploitability, threat activity, exposure, sensitivity, and control
    effectiveness must be clamped to `[0, 1]` after conversion.
-   Monetary values must not be negative. Negative values are treated as
    `0`.

Missing financial inputs are handled according to the **Financial
Impact** section rather than being fabricated.

------------------------------------------------------------------------

## 3. Probability Model

### 3.1 MVP base probability

The MVP uses a transparent CVSS-derived base probability:

**Base Probability = 0.05 + (CVSS / 10) × 0.35**

Therefore:

-   CVSS 0 → base probability = **0.05**
-   CVSS 10 → base probability = **0.40**

This is a deliberately bounded hackathon model. It is **not** a
calibrated actuarial or empirical breach-frequency model.

### 3.2 Adjustment factors

Define normalized factors:

-   `C` = asset criticality
-   `E` = internet exposure
-   `X` = exploitability
-   `T` = threat activity
-   `D` = data sensitivity

The combined risk multiplier is:

**Multiplier = 1 + 0.20C + 0.20E + 0.15X + 0.15T + 0.10D**

Maximum multiplier = **1.80**.

The pre-control probability is:

**Pre-Control Probability = Base Probability × Multiplier**

The result is then bounded to `[0, 1]`.

### 3.3 Control adjustment

Let `K` be control effectiveness from `0` to `1`.

**Incident Probability = Pre-Control Probability × (1 − K)**

Finally clamp the result to `[0, 1]`.

This model intentionally keeps the relationship simple and explainable:
stronger controls reduce the estimated probability proportionally.

### 3.4 Important assumption

The probability is an **annualized estimate for the MVP**. The model
does not claim that the probability is statistically calibrated to a
particular organization's historical incident frequency.

For production use, the coefficients and base rates would need
validation against organization-specific historical data and/or an
appropriate empirical dataset.

------------------------------------------------------------------------

## 4. Control Effectiveness

Control effectiveness is represented as a value from **0% to 100%**.

The MVP applies:

**Incident Probability = Pre-Control Probability × (1 − Control
Effectiveness)**

Expected behavior:

  -----------------------------------------------------------------------
                     Control effectiveness Probability effect
  ---------------------------------------- ------------------------------
                                    **0%** No reduction. Incident
                                           probability remains at the
                                           pre-control value.

                                   **50%** Probability is reduced by
                                           half.

                                  **100%** Probability becomes zero for
                                           the modeled risk.
  -----------------------------------------------------------------------

This does **not** mean a real-world control can guarantee prevention of
an incident. `100%` is an MVP modeling boundary representing complete
effectiveness within the modeled risk path.

Controls must not alter financial impact directly unless a scenario
explicitly changes an impact input.

------------------------------------------------------------------------

## 5. Financial Impact

The MVP defines:

**Financial Impact = Downtime Cost + Data Breach Cost + Recovery Cost +
Regulatory Cost + Reputation/Business Impact**

All components are expressed in INR.

### MVP treatment

The hackathon MVP uses **simulated financial values**. The data model
should keep the components separate even when they are generated from
demo fixtures.

Recommended MVP fixture fields:

-   `downtime_cost`
-   `data_breach_cost`
-   `recovery_cost`
-   `regulatory_cost`
-   `reputation_business_impact`

The sum is the incident financial impact.

### Missing financial data

The engine must **not invent a monetary value silently**.

If all financial components are missing, the financial impact is
reported as **unknown / unavailable**, and the corresponding EAL cannot
be presented as a valid monetary estimate.

If individual components are missing but other components are known, a
missing component may be treated as **0 only when the input explicitly
means "not applicable" or "none."** Missing/unknown data should
otherwise remain distinguishable from a genuine zero.

Financial values should be labeled as **simulated** whenever they
originate from MVP demo data.

------------------------------------------------------------------------

## 6. Expected Annual Loss

The authoritative formula is:

**EAL = Incident Probability × Financial Impact**

Example:

-   Incident probability = `0.20`
-   Financial impact = `₹10,00,000`

Then:

**EAL = 0.20 × ₹10,00,000 = ₹2,00,000**

EAL is an **estimated expected loss metric**, not a guaranteed loss and
not a prediction that exactly ₹2,00,000 will be lost.

EAL represents the modeled average annualized financial exposure under
the assumptions and inputs used by the engine.

------------------------------------------------------------------------

## 7. Enterprise Exposure

The MVP defines:

**Enterprise Exposure = Σ asset-level EALs**

The aggregation is performed over the set of **distinct modeled risk
exposures** included in the assessment.

### Avoiding double-counting

The MVP must avoid counting the same risk twice merely because multiple
technical findings refer to the same underlying risk.

For the hackathon implementation:

1.  Each finding must have a unique finding/risk identifier.
2.  Findings should be associated with a distinct asset and modeled risk
    path.
3.  If multiple findings are explicitly modeled as the **same risk
    event**, they must be consolidated before enterprise aggregation.
4.  Do not add both an already-aggregated asset EAL and its component
    finding EALs.
5.  Enterprise exposure must sum **one canonical EAL per modeled risk
    item**.

The UI should make clear whether a displayed EAL is at **finding, asset,
business-unit, or enterprise level**.

------------------------------------------------------------------------

## 8. Enterprise Risk Score

The MVP provides a normalized **0--100 Enterprise Risk Score**.

Let:

-   `Exposure` = enterprise EAL.
-   `ReferenceExposure` = configured reference annual exposure used to
    normalize the score.

The score is:

**Risk Score = min(100, 100 × Exposure / ReferenceExposure)**

`ReferenceExposure` must be a documented configuration value, not an
arbitrary value hidden in code.

For the hackathon demo, the reference exposure should be supplied by the
demo configuration/fixture so the score is deterministic and
reproducible.

### Thresholds

          Score Level
  ------------- ----------
      **0--24** Low
     **25--49** Moderate
     **50--74** High
    **75--100** Critical

The score is a **normalized communication metric**, not a probability
and not a replacement for EAL.

A zero exposure produces a score of `0 / Low`. Values at or above the
reference exposure cap at `100 / Critical`.

------------------------------------------------------------------------

## 9. Explainability

Every risk result must expose:

-   **Input values**
-   **Normalized input values**
-   **Intermediate values**
-   **Final result**
-   **Major risk drivers**
-   **Assumptions**

At minimum, the explanation should identify the strongest contributors
among CVSS, asset criticality, exposure, exploitability, threat
activity, data sensitivity, and control effectiveness.

### Example explanation

> **CVSS 9.8, internet exposure HIGH, asset criticality 5/5, and low
> control effectiveness increased the estimated incident probability.**

A detailed explanation should also be able to show:

-   CVSS normalization
-   base probability
-   each adjustment factor
-   pre-control probability
-   control effectiveness
-   final incident probability
-   each financial-impact component
-   total financial impact
-   EAL
-   confidence score
-   assumptions/data-quality warnings

The engine must never return a financial risk number without retaining
enough information to reproduce the calculation.

------------------------------------------------------------------------

## 10. Confidence

Confidence is a **data-completeness indicator**, not a claim that the
probability model is statistically accurate.

For each modeled risk item, define the required inputs:

1.  CVSS
2.  asset criticality
3.  financial value
4.  downtime cost
5.  internet exposure
6.  data sensitivity
7.  exploitability
8.  threat activity
9.  control effectiveness

Assign:

-   `1` when a required input is present and valid.
-   `0` when it is missing or invalid.

Then:

**Confidence = 100 × (number of present required inputs / 9)**

Round the displayed value to the nearest whole percentage point.

Example:

-   9/9 inputs → **100%**
-   7/9 inputs → **78%**
-   4/9 inputs → **44%**

The UI must label this as **data completeness/confidence**, not
"probability accuracy."

Missing financial information should additionally produce a visible
warning because EAL cannot be meaningfully computed without financial
impact.

------------------------------------------------------------------------

## 11. Scenario Calculations

Scenario analysis re-runs the **same deterministic risk pipeline** after
changing one or more inputs.

The engine must not create a separate hidden formula for scenarios.

### Control effectiveness scenario

Increase/decrease `K` and recompute:

**Incident Probability = Pre-Control Probability × (1 − K)**

Then recompute EAL.

Expected result:

**Higher control effectiveness → lower incident probability → lower
EAL**, with financial impact unchanged unless explicitly modified.

### Vulnerability-status scenario

If a vulnerability is remediated:

-   Remove the vulnerability from the active risk set, or
-   Set its modeled incident contribution to zero according to the
    application's canonical data model.

The result should reduce the corresponding risk contribution and
therefore enterprise exposure.

The exact representation must be consistent across the application.

### Exposure scenario

Change internet exposure from LOW/MEDIUM/HIGH and recompute the
probability pipeline.

Expected result:

**Higher exposure → higher probability → higher EAL**, assuming all
other inputs remain unchanged.

### Remediation scenario

A remediation scenario should change the relevant vulnerability/control
state and then run the same risk calculation again.

The scenario result should report:

-   baseline EAL
-   scenario EAL
-   absolute EAL reduction
-   percentage EAL reduction

Formula:

**EAL Reduction = Baseline EAL − Scenario EAL**

**EAL Reduction % = EAL Reduction / Baseline EAL × 100**

When baseline EAL is zero, percentage reduction should be reported as
**0% / not meaningful**, rather than dividing by zero.

------------------------------------------------------------------------

## 12. Testing

The following examples are normative checks for the MVP implementation.

### Example A --- CVSS 0

Inputs:

-   CVSS = `0`
-   Criticality = `1/5`
-   Exposure = `LOW`
-   Exploitability = `0`
-   Threat activity = `LOW`
-   Data sensitivity = `LOW`
-   Control effectiveness = `0%`

Calculations:

-   Base probability = `0.05`
-   Criticality factor `C = 0`
-   Exposure `E = 0`
-   Exploitability `X = 0`
-   Threat activity `T = 0`
-   Data sensitivity `D = 0`
-   Multiplier = `1.00`
-   Pre-control probability = `0.05`
-   Incident probability = `0.05`

**Expected incident probability: 0.05 (5%)**

This confirms that CVSS 0 does not automatically mean zero probability
in this MVP model; the model has a non-zero base rate.

### Example B --- CVSS 10

Inputs:

-   CVSS = `10`
-   Criticality = `5/5`
-   Exposure = `HIGH`
-   Exploitability = `1`
-   Threat activity = `1`
-   Data sensitivity = `1`
-   Control effectiveness = `0%`

Calculations:

-   Base probability = `0.40`
-   `C = E = X = T = D = 1`
-   Multiplier = `1 + 0.20 + 0.20 + 0.15 + 0.15 + 0.10 = 1.80`
-   Pre-control probability = `0.40 × 1.80 = 0.72`
-   Incident probability = `0.72`

**Expected incident probability: 0.72 (72%)**

### Example C --- 50% control effectiveness

Using Example B:

-   Pre-control probability = `0.72`
-   Control effectiveness = `0.50`

**Incident probability = 0.72 × (1 − 0.50) = 0.36**

**Expected incident probability: 0.36 (36%)**

### Example D --- 100% control effectiveness

Using Example B:

-   Pre-control probability = `0.72`
-   Control effectiveness = `1.00`

**Incident probability = 0.72 × 0 = 0**

**Expected incident probability: 0**

### Example E --- Financial impact and EAL

Inputs:

-   Incident probability = `0.20`
-   Downtime cost = `₹2,00,000`
-   Data breach cost = `₹5,00,000`
-   Recovery cost = `₹1,00,000`
-   Regulatory cost = `₹50,000`
-   Reputation/business impact = `₹1,50,000`

Financial impact:

**₹2,00,000 + ₹5,00,000 + ₹1,00,000 + ₹50,000 + ₹1,50,000 = ₹10,00,000**

EAL:

**0.20 × ₹10,00,000 = ₹2,00,000**

**Expected EAL: ₹2,00,000**

### Example F --- No financial data

If financial impact is unknown:

-   Financial Impact = **unknown**
-   EAL = **unknown / unavailable**
-   The engine must not silently substitute an arbitrary monetary value.

The risk engine may still calculate and display incident probability,
but monetary exposure must be clearly marked unavailable.

------------------------------------------------------------------------

## 13. Required Edge Cases

The implementation must test at least:

### CVSS = 0

-   Normalize to `0`.
-   Base probability must be `0.05`.
-   No division-by-zero or invalid probability.

### CVSS = 10

-   Normalize to `1`.
-   Base probability must be `0.40`.
-   With all adjustment factors at maximum and no controls, incident
    probability must be `0.72`.

### No financial data

-   Do not fabricate financial impact.
-   EAL must be unavailable unless sufficient financial-impact inputs
    exist.
-   UI must clearly identify the missing data.

### 100% control effectiveness

-   Final incident probability must be `0`.
-   EAL must therefore be `0` when financial impact is known.

### 0% control effectiveness

-   Final incident probability must equal the pre-control probability.
-   Control effectiveness must not accidentally increase or decrease the
    probability.

### Additional implementation edge cases

The engine should also handle:

-   CVSS below `0` or above `10` by clamping.
-   Criticality below `1` or above `5` by clamping.
-   Negative monetary inputs by treating them as `0`.
-   Probability values below `0` or above `1` by clamping.
-   Enterprise exposure with zero risk items → `0`.
-   Reference exposure of `0` must be rejected as invalid configuration
    rather than used as a denominator.
-   Baseline EAL of `0` in scenario percentage calculations must not
    cause division by zero.

------------------------------------------------------------------------

## 14. Source-of-Truth Implementation Rules

1.  **Do not introduce undocumented risk formulas.**
2.  Any coefficient or threshold used by the engine must be defined in
    this document or represented as explicit configuration with
    documented provenance.
3.  Keep all intermediate calculation values available for
    explainability.
4.  Keep simulated/demo financial data visibly separate from real
    telemetry.
5.  Do not represent EAL as guaranteed loss.
6.  Do not represent the 0--100 risk score as a probability.
7.  Do not call the confidence score a measure of model accuracy; it
    measures data completeness.
8.  Scenario calculations must re-use the canonical risk pipeline.
9.  Enterprise aggregation must use canonical, non-duplicated risk
    items.
10. If production requirements later demand statistically calibrated
    probabilities, update this specification before changing the
    implementation.

**This document is authoritative for CyberQuant AI risk calculations.**
