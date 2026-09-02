# CyberQuant AI — Deterministic Demo Dataset

## 1. Purpose

This document defines the deterministic synthetic enterprise dataset used by CyberQuant AI for demos, development, integration testing, and UI validation.

The dataset is intentionally fictional. It does **not** represent a real organization, real security incident, or real customer environment.

The dataset is designed to produce a coherent demo narrative:

1. The dashboard shows significant financial cyber-risk exposure.
2. Customer Database and Payment Gateway are among the largest contributors.
3. Missing MFA and critical vulnerabilities are major risk drivers.
4. The investment optimizer recommends high-value controls.
5. Scenario simulation materially reduces exposure.
6. The AI decision engine can explain the results using only the supplied data.

All IDs and numerical values are deterministic. A fresh database seeded from this document must produce the same demo results.

---

# 2. Dataset Principles

The demo dataset follows these principles:

- Synthetic only
- Deterministic
- Internally consistent
- Financially quantified
- Realistic enterprise naming
- No real organization references
- No real vulnerability claims
- Stable IDs
- Stable ordering
- Plausible CVSS scores
- Consistent INR units
- Compatible with the risk formulas defined in `docs/04-risk-engine.md`

The dataset should be stored in seed files or seed functions rather than generated randomly at runtime.

---

# 3. Dataset Size

The MVP demo dataset contains approximately:

| Entity | Target Count |
|---|---:|
| Assets | 40 |
| Vulnerabilities | 100 |
| Security Controls | 24 |
| Mitigation Actions | 20 |
| NIST Mappings | 50+ |

Exact counts should remain stable between demo runs.

---

# 4. Currency and Financial Units

All financial values are represented in INR.

Example:

```text
₹1 lakh = 100,000
₹10 lakh = 1,000,000
₹1 crore = 10,000,000
```

Database values must use numeric INR values.

Example:

```json
{
  "financial_value": 50000000,
  "downtime_cost": 1200000
}
```

The UI may format these as:

```text
₹5 crore
₹12 lakh
```

---

# 5. Deterministic IDs

Use stable IDs.

### Assets

```text
AST-001
AST-002
...
AST-040
```

### Vulnerabilities

```text
VUL-001
VUL-002
...
VUL-100
```

### Controls

```text
CTL-001
CTL-002
...
CTL-024
```

### Mitigations

```text
MIT-001
MIT-002
...
MIT-020
```

### NIST Controls

Use identifiers such as:

```text
NIST-CSF-ID.AM
NIST-CSF-PR.AA
NIST-CSF-PR.PS
NIST-CSF-DE.CM
NIST-CSF-RS.MA
NIST-CSF-RC.RP
```

---

# 6. Assets

The following 40 assets represent a fictional enterprise with Finance, Customer Operations, HR, Engineering, IT, Security, and Corporate functions.

| ID | Asset | Type | Business Unit | Criticality | Financial Value | Downtime Cost/Day | Internet Exposure | Data Sensitivity |
|---|---|---|---|---|---:|---:|---|---|
| AST-001 | Customer Database | Database | Customer Operations | Critical | 50000000 | 1500000 | No | Restricted |
| AST-002 | Payment Gateway | Application | Finance | Critical | 45000000 | 2200000 | Yes | Restricted |
| AST-003 | IAM Server | Identity Service | IT | Critical | 35000000 | 1800000 | Yes | Restricted |
| AST-004 | VPN Gateway | Network | IT | Critical | 30000000 | 1400000 | Yes | Confidential |
| AST-005 | Employee Portal | Web Application | HR | High | 12000000 | 500000 | Yes | Confidential |
| AST-006 | HR Database | Database | HR | High | 25000000 | 800000 | No | Restricted |
| AST-007 | CRM | Application | Sales | Critical | 32000000 | 1100000 | Yes | Confidential |
| AST-008 | ERP | Application | Finance | Critical | 40000000 | 1600000 | No | Restricted |
| AST-009 | Public API | API | Engineering | Critical | 38000000 | 1300000 | Yes | Confidential |
| AST-010 | Cloud Storage | Storage | Engineering | Critical | 42000000 | 1000000 | Yes | Restricted |
| AST-011 | Email Server | Messaging | Corporate IT | High | 18000000 | 700000 | Yes | Confidential |
| AST-012 | Data Warehouse | Database | Analytics | Critical | 36000000 | 900000 | No | Restricted |
| AST-013 | CI/CD Server | DevOps | Engineering | High | 16000000 | 600000 | Yes | Confidential |
| AST-014 | Source Code Repository | Repository | Engineering | High | 22000000 | 500000 | Yes | Confidential |
| AST-015 | Production Kubernetes Cluster | Compute | Engineering | Critical | 45000000 | 1800000 | Yes | Restricted |
| AST-016 | Internal Kubernetes Cluster | Compute | Engineering | High | 18000000 | 700000 | No | Confidential |
| AST-017 | Web Application Server | Compute | Engineering | High | 20000000 | 800000 | Yes | Confidential |
| AST-018 | Database Backup Server | Backup | IT | Critical | 30000000 | 1000000 | No | Restricted |
| AST-019 | SIEM Server | Security Platform | Security | High | 14000000 | 400000 | No | Confidential |
| AST-020 | EDR Management Server | Security Platform | Security | High | 10000000 | 350000 | No | Confidential |
| AST-021 | Active Directory | Identity Service | IT | Critical | 34000000 | 1700000 | No | Restricted |
| AST-022 | Privileged Access Server | Identity Service | Security | Critical | 28000000 | 1200000 | No | Restricted |
| AST-023 | File Server | Storage | Corporate IT | High | 15000000 | 550000 | No | Confidential |
| AST-024 | Intranet | Web Application | Corporate IT | Medium | 8000000 | 250000 | No | Internal |
| AST-025 | Payroll System | Application | HR | Critical | 24000000 | 900000 | No | Restricted |
| AST-026 | Procurement System | Application | Finance | High | 17000000 | 600000 | No | Confidential |
| AST-027 | Vendor Portal | Web Application | Procurement | High | 13000000 | 450000 | Yes | Confidential |
| AST-028 | Customer Support Portal | Web Application | Customer Operations | High | 21000000 | 700000 | Yes | Confidential |
| AST-029 | Analytics API | API | Analytics | Medium | 9000000 | 300000 | Yes | Confidential |
| AST-030 | Marketing Website | Web Application | Marketing | Medium | 6000000 | 200000 | Yes | Public |
| AST-031 | DNS Server | Network | IT | High | 11000000 | 500000 | Yes | Internal |
| AST-032 | Network Monitoring Server | Monitoring | IT | Medium | 7000000 | 250000 | No | Internal |
| AST-033 | Endpoint Management Server | Management | IT | High | 12000000 | 400000 | No | Confidential |
| AST-034 | HR Analytics Server | Analytics | HR | Medium | 10000000 | 300000 | No | Confidential |
| AST-035 | Finance Reporting Server | Analytics | Finance | High | 15000000 | 450000 | No | Confidential |
| AST-036 | Remote Desktop Gateway | Remote Access | IT | High | 18000000 | 750000 | Yes | Confidential |
| AST-037 | Internal API Gateway | API Gateway | Engineering | High | 20000000 | 700000 | No | Confidential |
| AST-038 | Container Registry | Repository | Engineering | High | 14000000 | 450000 | Yes | Confidential |
| AST-039 | Secrets Management Server | Security Platform | Security | Critical | 26000000 | 1100000 | No | Restricted |
| AST-040 | Disaster Recovery Site | Infrastructure | IT | Critical | 30000000 | 900000 | No | Restricted |

---

# 7. Asset Risk Distribution

The most financially important assets are intentionally:

1. Customer Database
2. Payment Gateway
3. Production Kubernetes Cluster
4. Cloud Storage
5. ERP
6. Public API
7. Data Warehouse
8. CRM

These assets have high financial values and/or high downtime costs.

The demo should therefore naturally show these assets near the top of financial-risk dashboards.

Customer Database and Payment Gateway should remain the most recognizable risk contributors.

---

# 8. Vulnerabilities

The dataset contains 100 synthetic vulnerability findings.

These are fictional findings created for demonstration purposes. They must never be presented as vulnerabilities discovered in a real company.

Each vulnerability should contain:

- ID
- title
- description
- asset ID
- CVSS score
- severity
- likelihood
- exploitability
- status
- NIST mapping

Example:

```json
{
  "id": "VUL-001",
  "title": "SQL Injection",
  "description": "Synthetic SQL injection finding for demo purposes.",
  "asset_id": "AST-001",
  "cvss_score": 9.8,
  "severity": "critical",
  "likelihood": 0.82,
  "exploitability": 0.90,
  "status": "open",
  "nist_category": "PR.PS"
}
```

---

# 9. Vulnerability Severity Rules

Use standard severity bands for synthetic CVSS values:

| CVSS | Severity |
|---:|---|
| 9.0–10.0 | Critical |
| 7.0–8.9 | High |
| 4.0–6.9 | Medium |
| 0.1–3.9 | Low |
| 0.0 | Informational |

The demo dataset should contain a mixture of severities.

Recommended distribution:

| Severity | Approx. Count |
|---|---:|
| Critical | 15 |
| High | 40 |
| Medium | 35 |
| Low | 10 |

---

# 10. Vulnerability Seed Data

The following 100 findings should be seeded deterministically.

| ID | Finding | Asset | CVSS | Severity | Likelihood | Status |
|---|---|---|---:|---|---:|---|
| VUL-001 | SQL Injection | AST-001 | 9.8 | Critical | 0.82 | Open |
| VUL-002 | Missing MFA | AST-001 | 9.1 | Critical | 0.78 | Open |
| VUL-003 | Excessive IAM Permissions | AST-001 | 8.8 | High | 0.70 | Open |
| VUL-004 | Outdated Database Component | AST-001 | 7.8 | High | 0.64 | Open |
| VUL-005 | Weak Password Policy | AST-001 | 7.5 | High | 0.66 | Open |
| VUL-006 | SQL Injection | AST-002 | 9.8 | Critical | 0.85 | Open |
| VUL-007 | Insecure API Configuration | AST-002 | 9.1 | Critical | 0.79 | Open |
| VUL-008 | Missing MFA | AST-002 | 8.9 | High | 0.76 | Open |
| VUL-009 | Outdated OpenSSL | AST-002 | 8.1 | High | 0.61 | Open |
| VUL-010 | Weak TLS Configuration | AST-002 | 7.4 | High | 0.55 | Open |
| VUL-011 | Missing MFA | AST-003 | 9.1 | Critical | 0.80 | Open |
| VUL-012 | Excessive IAM Permissions | AST-003 | 8.8 | High | 0.74 | Open |
| VUL-013 | Weak Password Policy | AST-003 | 7.5 | High | 0.68 | Open |
| VUL-014 | Outdated OpenSSL | AST-003 | 8.1 | High | 0.58 | Open |
| VUL-015 | Privileged Account Misconfiguration | AST-003 | 8.6 | High | 0.65 | Open |
| VUL-016 | Exposed RDP | AST-004 | 9.0 | Critical | 0.79 | Open |
| VUL-017 | Missing MFA | AST-004 | 9.1 | Critical | 0.81 | Open |
| VUL-018 | Outdated VPN Software | AST-004 | 8.2 | High | 0.65 | Open |
| VUL-019 | Weak Cipher Configuration | AST-004 | 6.8 | Medium | 0.50 | Open |
| VUL-020 | Missing EDR | AST-004 | 7.6 | High | 0.62 | Open |
| VUL-021 | Cross-Site Scripting | AST-005 | 7.2 | High | 0.52 | Open |
| VUL-022 | Weak Password Policy | AST-005 | 7.5 | High | 0.61 | Open |
| VUL-023 | Outdated Dependencies | AST-005 | 8.0 | High | 0.57 | Open |
| VUL-024 | Insecure Session Configuration | AST-005 | 6.5 | Medium | 0.46 | Open |
| VUL-025 | Publicly Accessible Admin Endpoint | AST-005 | 8.6 | High | 0.63 | Open |
| VUL-026 | Excessive Database Permissions | AST-006 | 8.1 | High | 0.64 | Open |
| VUL-027 | Missing Encryption at Rest | AST-006 | 7.4 | High | 0.52 | Open |
| VUL-028 | Missing MFA | AST-006 | 8.9 | High | 0.68 | Open |
| VUL-029 | Outdated Database Component | AST-006 | 7.8 | High | 0.58 | Open |
| VUL-030 | SQL Injection | AST-007 | 9.4 | Critical | 0.76 | Open |
| VUL-031 | Missing MFA | AST-007 | 8.9 | High | 0.72 | Open |
| VUL-032 | Outdated Dependencies | AST-007 | 8.0 | High | 0.59 | Open |
| VUL-033 | Broken Access Control | AST-007 | 8.7 | High | 0.67 | Open |
| VUL-034 | Insecure API Configuration | AST-007 | 7.9 | High | 0.55 | Open |
| VUL-035 | ERP Authorization Misconfiguration | AST-008 | 8.8 | High | 0.65 | Open |
| VUL-036 | Missing MFA | AST-008 | 8.9 | High | 0.70 | Open |
| VUL-037 | Outdated Dependencies | AST-008 | 7.8 | High | 0.54 | Open |
| VUL-038 | Excessive Privileges | AST-008 | 8.4 | High | 0.61 | Open |
| VUL-039 | Insecure API Configuration | AST-009 | 9.2 | Critical | 0.77 | Open |
| VUL-040 | Broken Access Control | AST-009 | 8.8 | High | 0.69 | Open |
| VUL-041 | SQL Injection | AST-009 | 9.5 | Critical | 0.81 | Open |
| VUL-042 | Outdated Dependencies | AST-009 | 8.0 | High | 0.58 | Open |
| VUL-043 | Missing Rate Limiting | AST-009 | 7.5 | High | 0.63 | Open |
| VUL-044 | Public Cloud Storage | AST-010 | 9.1 | Critical | 0.80 | Open |
| VUL-045 | Excessive IAM Permissions | AST-010 | 8.8 | High | 0.73 | Open |
| VUL-046 | Missing Encryption | AST-010 | 8.0 | High | 0.61 | Open |
| VUL-047 | Public Bucket Policy | AST-010 | 9.0 | Critical | 0.78 | Open |
| VUL-048 | Weak Access Controls | AST-010 | 7.6 | High | 0.62 | Open |
| VUL-049 | Outdated Mail Software | AST-011 | 8.1 | High | 0.56 | Open |
| VUL-050 | Missing MFA | AST-011 | 8.9 | High | 0.67 | Open |
| VUL-051 | Weak Password Policy | AST-011 | 7.5 | High | 0.59 | Open |
| VUL-052 | Phishing Exposure | AST-011 | 7.4 | High | 0.65 | Open |
| VUL-053 | Excessive Data Access | AST-012 | 8.2 | High | 0.58 | Open |
| VUL-054 | Missing Encryption | AST-012 | 7.9 | High | 0.55 | Open |
| VUL-055 | Weak Database Authentication | AST-012 | 8.0 | High | 0.60 | Open |
| VUL-056 | Outdated Dependencies | AST-013 | 8.0 | High | 0.55 | Open |
| VUL-057 | Exposed Management Interface | AST-013 | 8.5 | High | 0.60 | Open |
| VUL-058 | Missing MFA | AST-013 | 8.9 | High | 0.65 | Open |
| VUL-059 | Secrets in Build Configuration | AST-013 | 8.7 | High | 0.58 | Open |
| VUL-060 | Repository Credential Exposure | AST-014 | 8.8 | High | 0.62 | Open |
| VUL-061 | Missing Branch Protection | AST-014 | 6.8 | Medium | 0.45 | Open |
| VUL-062 | Excessive Repository Permissions | AST-014 | 7.8 | High | 0.55 | Open |
| VUL-063 | Vulnerable Container Image | AST-015 | 9.0 | Critical | 0.70 | Open |
| VUL-064 | Excessive Cluster Permissions | AST-015 | 8.8 | High | 0.65 | Open |
| VUL-065 | Missing Network Policies | AST-015 | 8.2 | High | 0.60 | Open |
| VUL-066 | Exposed Kubernetes API | AST-015 | 9.1 | Critical | 0.74 | Open |
| VUL-067 | Weak Service Account Permissions | AST-016 | 7.9 | High | 0.55 | Open |
| VUL-068 | Missing Network Segmentation | AST-016 | 7.5 | High | 0.51 | Open |
| VUL-069 | Outdated Container Images | AST-016 | 7.8 | High | 0.53 | Open |
| VUL-070 | Missing EDR | AST-017 | 7.6 | High | 0.60 | Open |
| VUL-071 | Outdated Web Server | AST-017 | 8.2 | High | 0.58 | Open |
| VUL-072 | Insecure Headers | AST-017 | 6.4 | Medium | 0.43 | Open |
| VUL-073 | Backup Exposure | AST-018 | 8.6 | High | 0.55 | Open |
| VUL-074 | Missing Immutable Backup | AST-018 | 8.9 | High | 0.60 | Open |
| VUL-075 | Excessive Backup Permissions | AST-018 | 7.7 | High | 0.50 | Open |
| VUL-076 | Missing Log Retention | AST-019 | 6.8 | Medium | 0.45 | Open |
| VUL-077 | Weak Administrator Authentication | AST-019 | 7.9 | High | 0.50 | Open |
| VUL-078 | Missing MFA | AST-020 | 8.9 | High | 0.62 | Open |
| VUL-079 | Outdated Management Software | AST-020 | 7.4 | High | 0.48 | Open |
| VUL-080 | Weak Domain Password Policy | AST-021 | 8.2 | High | 0.67 | Open |
| VUL-081 | Missing MFA | AST-021 | 9.1 | Critical | 0.78 | Open |
| VUL-082 | Excessive Domain Admin Permissions | AST-021 | 9.0 | Critical | 0.70 | Open |
| VUL-083 | Outdated Domain Services | AST-021 | 8.0 | High | 0.56 | Open |
| VUL-084 | Missing PAM | AST-022 | 9.0 | Critical | 0.74 | Open |
| VUL-085 | Excessive Privileged Access | AST-022 | 8.8 | High | 0.69 | Open |
| VUL-086 | Weak Administrator Authentication | AST-022 | 8.2 | High | 0.60 | Open |
| VUL-087 | Public File Share | AST-023 | 7.8 | High | 0.55 | Open |
| VUL-088 | Missing Encryption | AST-023 | 7.2 | High | 0.48 | Open |
| VUL-089 | Outdated File Server | AST-023 | 7.5 | High | 0.50 | Open |
| VUL-090 | Weak Authentication | AST-024 | 6.9 | Medium | 0.44 | Open |
| VUL-091 | Missing MFA | AST-025 | 8.9 | High | 0.65 | Open |
| VUL-092 | Excessive Payroll Permissions | AST-025 | 8.4 | High | 0.61 | Open |
| VUL-093 | Outdated Dependencies | AST-025 | 7.8 | High | 0.50 | Open |
| VUL-094 | Vendor Portal Injection | AST-027 | 8.8 | High | 0.62 | Open |
| VUL-095 | Missing MFA | AST-027 | 8.9 | High | 0.65 | Open |
| VUL-096 | Customer Portal XSS | AST-028 | 7.5 | High | 0.55 | Open |
| VUL-097 | Insecure API Configuration | AST-029 | 7.8 | High | 0.52 | Open |
| VUL-098 | DNS Configuration Weakness | AST-031 | 7.4 | High | 0.48 | Open |
| VUL-099 | Exposed RDP | AST-036 | 9.0 | Critical | 0.76 | Open |
| VUL-100 | Weak Secrets Management Configuration | AST-039 | 9.2 | Critical | 0.72 | Open |

Assets not directly represented above may still participate in the demo through controls, mitigations, and future seeded findings.

---

# 11. Security Controls

The dataset contains 24 security controls.

Each control should contain:

- ID
- name
- description
- category
- maturity
- effectiveness
- implementation status
- NIST mappings

| ID | Control | Category | Maturity | Effectiveness | Status |
|---|---|---|---|---:|---|
| CTL-001 | Multi-Factor Authentication | Identity | Partial | 0.90 | Partial |
| CTL-002 | Endpoint Detection and Response | Endpoint | Partial | 0.85 | Partial |
| CTL-003 | Web Application Firewall | Application Security | Partial | 0.82 | Partial |
| CTL-004 | Network Segmentation | Network | Partial | 0.88 | Partial |
| CTL-005 | Patch Management | Vulnerability Management | Partial | 0.86 | Partial |
| CTL-006 | Privileged Access Management | Identity | Limited | 0.92 | Partial |
| CTL-007 | Centralized Logging | Detection | Partial | 0.75 | Implemented |
| CTL-008 | Immutable Backup | Recovery | Partial | 0.90 | Partial |
| CTL-009 | Encryption at Rest | Data Protection | Partial | 0.88 | Partial |
| CTL-010 | Vulnerability Management | Vulnerability Management | Partial | 0.84 | Implemented |
| CTL-011 | Email Security | Email Security | Partial | 0.78 | Partial |
| CTL-012 | Secure Configuration Management | Configuration | Partial | 0.82 | Partial |
| CTL-013 | API Security Gateway | Application Security | Limited | 0.84 | Partial |
| CTL-014 | Cloud Security Posture Management | Cloud Security | Limited | 0.87 | Partial |
| CTL-015 | Secrets Management | Application Security | Partial | 0.90 | Partial |
| CTL-016 | Security Awareness Training | Human Security | Partial | 0.65 | Implemented |
| CTL-017 | Data Loss Prevention | Data Protection | Limited | 0.75 | Partial |
| CTL-018 | Intrusion Detection | Network Detection | Partial | 0.72 | Implemented |
| CTL-019 | Backup Recovery Testing | Recovery | Limited | 0.80 | Partial |
| CTL-020 | Incident Response | Response | Partial | 0.78 | Implemented |
| CTL-021 | Asset Inventory | Governance | Implemented | 0.85 | Implemented |
| CTL-022 | Security Monitoring | Detection | Partial | 0.82 | Implemented |
| CTL-023 | Database Activity Monitoring | Database Security | Limited | 0.76 | Partial |
| CTL-024 | Zero Trust Access | Identity/Network | Limited | 0.88 | Partial |

---

# 12. Mitigation Actions

Mitigation actions represent potential investments that the Investment Optimization Engine can evaluate.

All costs and risk reductions are deterministic and expressed in INR.

| ID | Mitigation | Cost | Expected Risk Reduction | Implementation Time | Priority |
|---|---|---:|---:|---:|---|
| MIT-001 | Enterprise MFA Rollout | 200000 | 10000000 | 14 days | Critical |
| MIT-002 | Critical Vulnerability Patching | 100000 | 9000000 | 10 days | Critical |
| MIT-003 | EDR Expansion | 400000 | 6000000 | 21 days | High |
| MIT-004 | Network Segmentation | 500000 | 8000000 | 30 days | High |
| MIT-005 | Privileged Access Management Rollout | 350000 | 7000000 | 25 days | Critical |
| MIT-006 | WAF Hardening | 250000 | 5000000 | 14 days | High |
| MIT-007 | Cloud Storage Remediation | 150000 | 5500000 | 7 days | Critical |
| MIT-008 | API Security Hardening | 200000 | 4500000 | 14 days | High |
| MIT-009 | Database Encryption Upgrade | 300000 | 4000000 | 21 days | High |
| MIT-010 | Immutable Backup Deployment | 350000 | 6500000 | 21 days | Critical |
| MIT-011 | Vulnerability Management Automation | 180000 | 3500000 | 14 days | High |
| MIT-012 | Secure Configuration Baseline | 120000 | 2800000 | 10 days | Medium |
| MIT-013 | Email Security Upgrade | 220000 | 3200000 | 14 days | High |
| MIT-014 | Secrets Management Upgrade | 250000 | 4200000 | 18 days | Critical |
| MIT-015 | Centralized Logging Expansion | 180000 | 3000000 | 14 days | Medium |
| MIT-016 | PAM for Tier-0 Accounts | 150000 | 3500000 | 10 days | Critical |
| MIT-017 | Kubernetes Security Hardening | 300000 | 5000000 | 21 days | High |
| MIT-018 | Database Activity Monitoring | 280000 | 3000000 | 20 days | Medium |
| MIT-019 | Incident Response Automation | 200000 | 2500000 | 21 days | Medium |
| MIT-020 | Employee Security Awareness Program | 100000 | 1800000 | 30 days | Medium |

---

# 13. Investment Efficiency

The optimizer calculates:

```text
Risk Reduction per Rupee =
Expected Risk Reduction / Cost
```

Using the mitigation dataset:

| ID | Mitigation | Cost | Risk Reduction | Reduction / Rupee |
|---|---|---:|---:|---:|
| MIT-001 | Enterprise MFA Rollout | ₹2,00,000 | ₹1,00,00,000 | 50.00 |
| MIT-002 | Critical Vulnerability Patching | ₹1,00,000 | ₹90,00,000 | 90.00 |
| MIT-003 | EDR Expansion | ₹4,00,000 | ₹60,00,000 | 15.00 |
| MIT-004 | Network Segmentation | ₹5,00,000 | ₹80,00,000 | 16.00 |
| MIT-005 | PAM Rollout | ₹3,50,000 | ₹70,00,000 | 20.00 |
| MIT-006 | WAF Hardening | ₹2,50,000 | ₹50,00,000 | 20.00 |
| MIT-007 | Cloud Storage Remediation | ₹1,50,000 | ₹55,00,000 | 36.67 |
| MIT-008 | API Security Hardening | ₹2,00,000 | ₹45,00,000 | 22.50 |
| MIT-009 | Database Encryption | ₹3,00,000 | ₹40,00,000 | 13.33 |
| MIT-010 | Immutable Backup | ₹3,50,000 | ₹65,00,000 | 18.57 |

The exact optimizer result depends on the supplied budget and the remaining investment options.

---

# 14. Recommended Demo Budget

For the standard optimizer demo, use:

```text
₹5,00,000
```

The greedy optimizer should rank actions primarily by risk reduction per rupee.

For the first few actions:

```text
MIT-002 = 90.00
MIT-001 = 50.00
MIT-007 = 36.67
MIT-008 = 22.50
MIT-005 = 20.00
MIT-006 = 20.00
MIT-010 = 18.57
MIT-004 = 16.00
MIT-003 = 15.00
MIT-009 = 13.33
```

With a ₹5 lakh budget, the greedy sequence is:

1. Critical Vulnerability Patching — ₹1 lakh
2. Enterprise MFA Rollout — ₹2 lakh
3. Cloud Storage Remediation — ₹1.5 lakh

Remaining:

```text
₹5 lakh - ₹1 lakh - ₹2 lakh - ₹1.5 lakh
= ₹50,000
```

The next available actions exceed the remaining budget, so the optimizer stops.

Expected selected investment:

```text
MIT-002
MIT-001
MIT-007
```

Total investment:

```text
₹4,50,000
```

Expected risk reduction:

```text
₹90,00,000
+ ₹1,00,00,000
+ ₹55,00,000
= ₹2,45,00,000
```

Remaining budget:

```text
₹50,000
```

---

# 15. Risk Engine Compatibility

The dataset must use the same risk concepts and units defined in:

```text
docs/04-risk-engine.md
```

The demo data should support financial risk calculations based on the existing risk engine rather than introducing a separate competing formula.

Where the risk engine uses:

```text
Expected Loss = Probability × Financial Impact
```

the demo data must provide compatible probability/likelihood and financial-impact inputs.

Where vulnerability severity contributes to likelihood, CVSS values should be used as supporting technical severity data rather than being treated directly as INR loss.

---

# 16. Asset-to-Risk Relationship

The dataset intentionally concentrates high-impact risks around critical assets.

### Customer Database

Primary drivers:

- SQL Injection
- Missing MFA
- Excessive IAM Permissions
- Weak Password Policy
- Outdated Database Components

### Payment Gateway

Primary drivers:

- SQL Injection
- Insecure API Configuration
- Missing MFA
- Outdated OpenSSL
- Weak TLS Configuration

### IAM Server

Primary drivers:

- Missing MFA
- Excessive IAM Permissions
- Weak Password Policy
- Outdated OpenSSL
- Privileged Account Misconfiguration

### VPN Gateway

Primary drivers:

- Exposed RDP
- Missing MFA
- Outdated VPN Software
- Weak Cipher Configuration
- Missing EDR

### Cloud Storage

Primary drivers:

- Public Cloud Storage
- Public Bucket Policy
- Excessive IAM Permissions
- Missing Encryption
- Weak Access Controls

These relationships ensure that the dashboard can explain why specific assets contribute heavily to exposure.

---

# 17. NIST Framework Mappings

The dataset should map assets, vulnerabilities, controls, and mitigations to NIST Cybersecurity Framework concepts.

The mappings are synthetic and intended for demonstration.

## 17.1 Asset Management

```text
AST-001 -> ID.AM
AST-002 -> ID.AM
AST-003 -> ID.AM
AST-009 -> ID.AM
AST-010 -> ID.AM
AST-015 -> ID.AM
AST-021 -> ID.AM
AST-039 -> ID.AM
```

## 17.2 Identity Management

```text
VUL-002 -> PR.AA
VUL-008 -> PR.AA
VUL-011 -> PR.AA
VUL-017 -> PR.AA
VUL-081 -> PR.AA
VUL-084 -> PR.AA

CTL-001 -> PR.AA
CTL-006 -> PR.AA
CTL-024 -> PR.AA

MIT-001 -> PR.AA
MIT-005 -> PR.AA
MIT-016 -> PR.AA
```

## 17.3 Platform Security

```text
VUL-004 -> PR.PS
VUL-009 -> PR.PS
VUL-023 -> PR.PS
VUL-037 -> PR.PS
VUL-056 -> PR.PS
VUL-063 -> PR.PS
VUL-071 -> PR.PS

CTL-005 -> PR.PS
CTL-012 -> PR.PS
CTL-014 -> PR.PS

MIT-002 -> PR.PS
MIT-011 -> PR.PS
MIT-012 -> PR.PS
MIT-017 -> PR.PS
```

## 17.4 Data Security

```text
VUL-027 -> PR.DS
VUL-044 -> PR.DS
VUL-046 -> PR.DS
VUL-047 -> PR.DS
VUL-054 -> PR.DS
VUL-088 -> PR.DS

CTL-009 -> PR.DS
CTL-017 -> PR.DS
CTL-023 -> PR.DS

MIT-007 -> PR.DS
MIT-009 -> PR.DS
```

## 17.5 Continuous Monitoring

```text
VUL-076 -> DE.CM
VUL-077 -> DE.CM
VUL-078 -> DE.CM

CTL-007 -> DE.CM
CTL-018 -> DE.CM
CTL-022 -> DE.CM

MIT-015 -> DE.CM
MIT-018 -> DE.CM
```

## 17.6 Incident Response

```text
CTL-020 -> RS.MA
MIT-019 -> RS.MA
```

## 17.7 Recovery

```text
VUL-073 -> RC.RP
VUL-074 -> RC.RP
VUL-075 -> RC.RP

CTL-008 -> RC.RP
CTL-019 -> RC.RP

MIT-010 -> RC.RP
```

---

# 18. Example NIST Mapping Object

Mappings should be represented in a machine-readable structure.

```json
{
  "entity_type": "mitigation",
  "entity_id": "MIT-001",
  "framework": "NIST-CSF",
  "function": "Protect",
  "category": "PR.AA"
}
```

Another example:

```json
{
  "entity_type": "vulnerability",
  "entity_id": "VUL-044",
  "framework": "NIST-CSF",
  "function": "Protect",
  "category": "PR.DS"
}
```

---

# 19. Demo Narrative

## Step 1 — Dashboard

The dashboard should initially show:

- High total financial exposure
- High critical-risk count
- High-risk assets
- Open critical vulnerabilities
- Top risk contributors
- Security-control coverage

The most important visual contributors should include:

```text
Customer Database
Payment Gateway
IAM Server
Cloud Storage
Production Kubernetes Cluster
ERP
Public API
```

---

## Step 2 — Top Risk Contributors

The dashboard should make it possible to drill into:

### Customer Database

Primary issues:

```text
SQL Injection
Missing MFA
Excessive IAM Permissions
Weak Password Policy
```

### Payment Gateway

Primary issues:

```text
SQL Injection
Insecure API Configuration
Missing MFA
Outdated OpenSSL
```

The system should explain the financial impact using the risk engine's calculated exposure.

---

## Step 3 — Vulnerability View

The vulnerability dashboard should show:

- Critical vulnerabilities
- High vulnerabilities
- CVSS distribution
- Affected assets
- Risk contribution
- Remediation status

Critical findings should be visible at the top.

Important demo findings include:

```text
VUL-001 SQL Injection
VUL-002 Missing MFA
VUL-006 SQL Injection
VUL-007 Insecure API Configuration
VUL-011 Missing MFA
VUL-044 Public Cloud Storage
VUL-047 Public Bucket Policy
VUL-063 Vulnerable Container Image
VUL-066 Exposed Kubernetes API
VUL-081 Missing MFA
VUL-082 Excessive Domain Admin Permissions
VUL-084 Missing PAM
VUL-099 Exposed RDP
VUL-100 Weak Secrets Management Configuration
```

---

# 20. Optimizer Demo

Use:

```text
Budget = ₹5,00,000
```

The optimizer calculates risk reduction per rupee and selects:

```text
Critical Vulnerability Patching
Enterprise MFA Rollout
Cloud Storage Remediation
```

Expected financial results:

```text
Total investment = ₹4,50,000

Expected risk reduction = ₹2,45,00,000

Remaining budget = ₹50,000
```

If the current exposure is at least ₹2.45 crore, the scenario should show a substantial reduction without producing negative exposure.

---

# 21. Scenario Simulation

The scenario engine should be able to calculate:

```text
Before Exposure
        ↓
Apply Selected Mitigations
        ↓
After Exposure
```

Formula:

```text
After Exposure =
max(0, Before Exposure - Expected Risk Reduction)
```

The simulation must not mutate the original baseline data.

Example:

```json
{
  "scenario": "₹5 lakh security investment",
  "before_exposure": 30000000,
  "investment": 450000,
  "expected_risk_reduction": 24500000,
  "after_exposure": 5500000
}
```

Percentage reduction:

```text
(24,500,000 / 30,000,000) × 100
= 81.67%
```

ROSI:

```text
((24,500,000 - 450,000) / 450,000) × 100
= 5,344.44%
```

These values are synthetic demo calculations.

---

# 22. AI Explanation Demo

The AI decision engine should be able to answer:

### "What is our highest financial cyber risk?"

Expected response should reference the calculated dataset and identify the highest contributing asset/risk rather than inventing an answer.

Example:

```text
The Customer Database is one of the highest financial-risk assets
because it combines high financial value with multiple critical and
high-severity findings, including SQL Injection and Missing MFA.
```

### "What should we fix first?"

Expected explanation:

```text
Critical Vulnerability Patching is ranked first because its expected
risk reduction per rupee is the highest among the available mitigation
actions.
```

### "How much risk can we reduce with ₹5 lakh?"

The AI should report the deterministic optimizer result:

```text
The current demo dataset allocates ₹4.5 lakh to three actions and
projects ₹2.45 crore of expected risk reduction, leaving ₹50,000
unused.
```

The AI must not change these numbers.

---

# 23. Deterministic Seeding

The backend should expose a deterministic seed operation for local development.

Suggested command:

```bash
python -m app.seed_demo_data
```

The seed operation should:

1. Clear existing demo records.
2. Insert assets in fixed ID order.
3. Insert vulnerabilities in fixed ID order.
4. Insert controls in fixed ID order.
5. Insert mitigation actions in fixed ID order.
6. Insert NIST mappings in fixed order.
7. Commit the transaction.
8. Produce the same dataset every time.

Do not use:

```python
random.random()
```

or time-based IDs.

If deterministic random generation is ever required, use an explicit fixed seed such as:

```python
random.seed(20260902)
```

However, explicitly defined seed data is preferred over random generation.

---

# 24. Demo Dataset Integrity Checks

After seeding, validate:

```text
asset_count = 40
vulnerability_count = 100
control_count = 24
mitigation_count = 20
```

Also validate:

- All asset IDs are unique.
- All vulnerability IDs are unique.
- All control IDs are unique.
- All mitigation IDs are unique.
- Every vulnerability references an existing asset.
- Every affected asset references an existing asset.
- Every affected risk references a valid risk.
- Every NIST mapping references an existing entity.
- Costs are non-negative.
- Expected risk reductions are non-negative.
- CVSS values are between 0 and 10.
- Criticality values are valid.
- Data sensitivity values are valid.

---

# 25. Referential Integrity

Example:

```json
{
  "id": "MIT-007",
  "name": "Cloud Storage Remediation",
  "affected_assets": [
    "AST-010"
  ],
  "affected_risks": [
    "VUL-044",
    "VUL-047"
  ]
}
```

Every referenced ID must exist.

Invalid references must cause seed validation to fail.

The application must not silently create orphan relationships.

---

# 26. Recommended Data Files

The implementation may split the dataset into:

```text
data/
├── demo_assets.json
├── demo_vulnerabilities.json
├── demo_controls.json
├── demo_mitigations.json
└── demo_nist_mappings.json
```

Alternatively, a single deterministic fixture can be used:

```text
data/
└── cyberquant_demo.json
```

For the MVP, a single fixture file is acceptable if it remains maintainable.

---

# 27. Example Combined Fixture Structure

```json
{
  "metadata": {
    "dataset": "CyberQuant AI Synthetic Enterprise",
    "version": "1.0",
    "generated": "static",
    "synthetic": true
  },
  "assets": [],
  "vulnerabilities": [],
  "controls": [],
  "mitigations": [],
  "nist_mappings": []
}
```

The `generated` field should describe the dataset as static rather than recording the current runtime timestamp.

---

# 28. No Real-Organization Claims

The application must clearly treat this dataset as synthetic.

Recommended UI disclaimer:

```text
Demo Environment — All assets, vulnerabilities, financial values,
and risk calculations are synthetic and created for demonstration
purposes only. They do not represent a real organization.
```

Do not display statements such as:

```text
"We discovered SQL Injection in the company's Customer Database."
```

Instead:

```text
"The synthetic demo dataset contains a SQL Injection finding
associated with the Customer Database."
```

---

# 29. Consistency Requirements

The following must remain consistent across all demo modules:

```text
Assets
   ↓
Vulnerabilities
   ↓
Risk Engine
   ↓
Risk Exposure
   ↓
Mitigations
   ↓
Investment Optimizer
   ↓
Scenario Simulation
   ↓
AI Explanation
```

Do not create separate hard-coded numbers for the dashboard, optimizer, and AI.

All modules should read from the same seeded data and deterministic calculation services.

---

# 30. MVP Acceptance Criteria

The demo dataset is complete when:

- [ ] Approximately 40 assets exist.
- [ ] Approximately 100 vulnerabilities exist.
- [ ] 24 security controls exist.
- [ ] 20 mitigation actions exist.
- [ ] NIST mappings exist.
- [ ] All data is synthetic.
- [ ] All IDs are deterministic.
- [ ] All financial values use INR.
- [ ] CVSS scores are plausible.
- [ ] Customer Database is a major risk contributor.
- [ ] Payment Gateway is a major risk contributor.
- [ ] Missing MFA is a major risk driver.
- [ ] Critical vulnerabilities are visible in the dashboard.
- [ ] Mitigations affect relevant assets and risks.
- [ ] Optimizer can use the mitigation dataset.
- [ ] The ₹5 lakh demo budget produces a consistent recommendation.
- [ ] Scenario simulation produces a materially lower exposure.
- [ ] No calculated exposure becomes negative.
- [ ] AI explanations use calculated values rather than invented values.
- [ ] Dataset can be reseeded and produce identical results.
- [ ] No demo data is presented as belonging to a real organization.

---

# 31. Summary

The CyberQuant AI demo dataset represents a fictional enterprise with:

```text
40 Assets
100 Vulnerabilities
24 Security Controls
20 Mitigation Actions
50+ NIST Framework Mappings
```

The dataset deliberately concentrates significant financial exposure around:

```text
Customer Database
Payment Gateway
IAM Server
Cloud Storage
Production Kubernetes Cluster
ERP
Public API
```

It also provides a consistent investment scenario:

```text
Budget = ₹5,00,000

Selected:
- Critical Vulnerability Patching
- Enterprise MFA Rollout
- Cloud Storage Remediation

Total Investment = ₹4,50,000
Expected Risk Reduction = ₹2,45,00,000
Remaining Budget = ₹50,000
```

The complete dataset is synthetic, deterministic, and designed to work consistently across the dashboard, risk engine, vulnerability view, investment optimizer, scenario simulator, NIST mapping view, and AI decision-support layer.
