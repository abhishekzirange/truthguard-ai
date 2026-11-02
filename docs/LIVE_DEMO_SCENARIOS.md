# TruthGuard AI — Real-World Demonstration Scenarios

**Evaluation Type:** End-to-End Factual Verification Walkthrough  
**Date:** 2026-11-02 17:33:51 UTC  
**Execution Pipeline:** Multi-Stage Claim Extraction, Disambiguated Retrieval, Deterministic SemVer/Consensus, & Mathematical Freshness Decay  

## Scenario 1: Outdated Software Version

- **Domain:** `software_version`
- **Execution Mode:** `OFFLINE` (Provenance: `OFFLINE_DETERMINISTIC`)
- **Measured Latency:** 33 ms
- **Billed External Tokens:** 0 in / 0 out ($0.000000 USD)

### 1. Input Answer
> "Python 3.11 is the latest stable Python release recommended for new production projects."

### 2. Extracted Claim & Atomic Triple
- **Claim:** "Python 3.11 is the latest stable Python release recommended for new production projects."
- **Subject:** `Python 3.11`
- **Predicate:** `is the latest`
- **Object:** `stable Python release recommended for new production projects.`
- **Mentioned Version:** `3.11`

### 3. Evidence Retrieved
- **[Python Release Python 3.13.2 and 3.12.9](https://www.python.org/downloads/release/python-3132/)** (`python.org`) — *Published: 2024-10-07T12:00:00*
  > "Python 3.13 is the newest major release of Python, successfully launched in October 2024. Python 3.12 is stable. Python 3.11 is now in secur..."
- **[Python.org Official Release Schedule & Status](https://devguide.python.org/versions/)** (`devguide.python.org`) — *Published: 2024-10-15T00:00:00*
  > "Python 3.13: bugfix / stable. Python 3.12: bugfix / stable. Python 3.11: security mode only, end of regular bugfix support was reached in Oc..."

### 4. Verification Verdict & Scores
- **Verdict:** **`OUTDATED`**
- **Freshness Score:** 0.0%
- **Evidence Quality Score:** 67.5%
- **Reasoning:** [OFFLINE DETERMINISTIC] Claimed version 3.11 is superseded by official release 3.13.2.
- **Suggested Evidence-Backed Correction:** *"Python 3.13.2 is the current release."*

---

## Scenario 2: Changing Product Price

- **Domain:** `pricing`
- **Execution Mode:** `OFFLINE` (Provenance: `OFFLINE_DETERMINISTIC`)
- **Measured Latency:** 30 ms
- **Billed External Tokens:** 0 in / 0 out ($0.000000 USD)

### 1. Input Answer
> "OpenAI flagship GPT-4 costs $30.00 per 1M input tokens and $60.00 per 1M output tokens."

### 2. Extracted Claim & Atomic Triple
- **Claim:** "OpenAI flagship GPT-4 costs $30.00 per 1M input tokens and $60.00 per 1M output tokens."
- **Subject:** `OpenAI flagship GPT-4`
- **Predicate:** `costs`
- **Object:** `$30.00 per 1M input tokens and $60.00 per 1M output tokens.`
- **Mentioned Version:** `4`

### 3. Evidence Retrieved
- **[OpenAI Pricing: Models and API Rates](https://openai.com/api/pricing/)** (`openai.com`) — *Published: 2024-10-01T00:00:00*
  > "GPT-4o pricing is $2.50 per 1M input tokens and $10.00 per 1M output tokens. Legacy GPT-4 pricing was $30 per 1M input tokens and has been s..."
- **[OpenAI Company Overview & Leadership](https://openai.com/about/)** (`openai.com`) — *Published: 2024-11-01T00:00:00*
  > "Sam Altman is the CEO of OpenAI."

### 4. Verification Verdict & Scores
- **Verdict:** **`CONTRADICTED`**
- **Freshness Score:** 0.0%
- **Evidence Quality Score:** 71.4%
- **Reasoning:** [OFFLINE DETERMINISTIC] Claimed price ($30.0) conflicts with published pricing ($2.5).
- **Suggested Evidence-Backed Correction:** *"Current official price is $2.5."*

---

## Scenario 3: Regulation with Relevant Amendment

- **Domain:** `regulation`
- **Execution Mode:** `OFFLINE` (Provenance: `OFFLINE_HEURISTIC_ANALYSIS`)
- **Measured Latency:** 21 ms
- **Billed External Tokens:** 0 in / 0 out ($0.000000 USD)

### 1. Input Answer
> "The EU-US Privacy Shield is an active and valid legal framework for commercial personal data transfers from the European Union to the United States."

### 2. Extracted Claim & Atomic Triple
- **Claim:** "The EU-US Privacy Shield is an active and valid legal framework for commercial personal data transfers from the European Union to the United States."
- **Subject:** `The EU-US Privacy Shield`
- **Predicate:** `is`
- **Object:** `an active and valid legal framework for commercial personal data transfers from the European Union to the United States.`

### 3. Evidence Retrieved
- **[Court of Justice of the European Union: Schrems II Judgment](https://curia.europa.eu/jcms/jcms/p1_3160867/en/)** (`curia.europa.eu`) — *Published: 2023-07-10T00:00:00*
  > "The Court of Justice invalidates Decision 2016/1250 on the adequacy of the protection provided by the EU-US Privacy Shield. The EU-US Data P..."

### 4. Verification Verdict & Scores
- **Verdict:** **`OUTDATED`**
- **Freshness Score:** 31.6%
- **Evidence Quality Score:** 63.8%
- **Reasoning:** [OFFLINE HEURISTIC ANALYSIS - Live Bifrost Gateway Unavailable] Authoritative governmental and legal records indicate this legal or treaty status has officially changed.
- **Suggested Evidence-Backed Correction:** *"Update to the current treaty, membership, or statutory regulatory framework."*

---

## Scenario 4: Old Company Leadership Claim

- **Domain:** `company_info`
- **Execution Mode:** `OFFLINE` (Provenance: `OFFLINE_HEURISTIC_ANALYSIS`)
- **Measured Latency:** 21 ms
- **Billed External Tokens:** 0 in / 0 out ($0.000000 USD)

### 1. Input Answer
> "Twitter is led and operated by Chief Executive Officer Jack Dorsey, who oversees the platform daily operations."

### 2. Extracted Claim & Atomic Triple
- **Claim:** "Twitter is led and operated by Chief Executive Officer Jack Dorsey, who oversees the platform daily operations."
- **Subject:** `Twitter`
- **Predicate:** `is`
- **Object:** `led and operated by Chief Executive Officer Jack Dorsey, who oversees the platform daily operations.`

### 3. Evidence Retrieved
- **[X / Twitter Leadership and Executive Structure](https://about.x.com/)** (`about.x.com`) — *Published: 2024-06-01T00:00:00*
  > "Linda Yaccarino serves as the Chief Executive Officer of X (formerly Twitter). Jack Dorsey stepped down as CEO in November 2021. Parag Agraw..."

### 4. Verification Verdict & Scores
- **Verdict:** **`OUTDATED`**
- **Freshness Score:** 43.2%
- **Evidence Quality Score:** 64.4%
- **Reasoning:** [OFFLINE HEURISTIC ANALYSIS - Live Bifrost Gateway Unavailable] Authoritative corporate records indicate the specified leader has stepped down, been succeeded, or departed the role.
- **Suggested Evidence-Backed Correction:** *"Update to the current appointed executive or leadership."*

---

## Scenario 5: Old Technical Claim That Remains Correct

- **Domain:** `technology`
- **Execution Mode:** `OFFLINE` (Provenance: `OFFLINE_DETERMINISTIC`)
- **Measured Latency:** 18 ms
- **Billed External Tokens:** 0 in / 0 out ($0.000000 USD)

### 1. Input Answer
> "Kubernetes 1.20 deprecated dockershim as a container runtime in favor of direct CRI implementations."

### 2. Extracted Claim & Atomic Triple
- **Claim:** "Kubernetes 1.20 deprecated dockershim as a container runtime in favor of direct CRI implementations."
- **Subject:** `Kubernetes`
- **Predicate:** `1.20 deprecated`
- **Object:** `dockershim as a container runtime in favor of direct CRI implementations.`
- **Mentioned Version:** `1.20`

### 3. Evidence Retrieved
- **[Kubernetes Release History](https://kubernetes.io/releases/)** (`kubernetes.io`) — *Published: 2024-08-13T00:00:00*
  > "Kubernetes 1.31 and 1.30 are active releases. Kubernetes 1.20 deprecated dockershim, which was removed in 1.24. Kubernetes 1.15 is long obso..."

### 4. Verification Verdict & Scores
- **Verdict:** **`CURRENT`**
- **Freshness Score:** 0.0%
- **Evidence Quality Score:** 56.5%
- **Reasoning:** [OFFLINE DETERMINISTIC] Historical milestone for version 1.20 is corroborated by documentation.

---

