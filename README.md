# Structured Logic Disclosure for 2026 Code of Practice
## Project: IfThenWhy™ Logic RFC (v1.0.0)
### NIST-2025-0035 & April 2nd Concept Paper Alignment

[![NIST Aligned](https://img.shields.io/badge/NIST-mme--5c57--j61h-blue)](https://www.regulations.gov/comment/NIST-2025-0035)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Status: USPTO Pending](https://img.shields.io/badge/Trademark-1/10/26-orange)](https://www.uspto.gov)

## A Framework for Deterministic Data Grounding

This repository serves as the official machine-readable reference implementation for the **Logic RFC™** protocol. It is designed to meet the **Technical Control** requirements of the **EU AI Act (Article 11 & 12)** and the **2026 NIST AI Agent Standards (Identity & Authorization Focus)**. 

Unlike probabilistic RAG (Retrieval-Augmented Generation), this framework provides **Deterministic Grounding** by anchoring AI agentic reasoning to a fixed symbolic logic layer.

### 🏛️ Prior Art & Authority
This framework has been formally submitted for public record to:
* **NIST:** (Regulations.gov) - Docket NIST-2025-0035: Technical Controls for AI Safety.
* **NIST AI 800-2:** Practices for Automated Benchmark Evaluations (Addressing requirements for external validity and deterministic mathematical truth).
* **NIST/NCCoE:** April 2nd Concept Paper on AI Agent Identity & Authorization (Focusing on metadata identity and non-repudiation).
* **W3C:** AI Content Disclosure Community Group (March 2026).

### 🎯 The "IfThenWhy" Intent
The Logic RFC uses a architecture to ensure that every data action taken by an AI agent is authorized, audited, and mathematically verified.

1.  **Metric Manifest (MAN):** The "Master Label" and **Identity Anchor**. Defines the ITW_ID, Version, and Business Owner.
2.  **Semantic Layer (SEM):** The "Business Why". Natural language manifests that anchor every metric to a specific Stakeholder Persona.
3.  **Bridge File (BRG):** The **Kinetic Link**. Maps the business trigger (If) to the data action (Then). 
4.  **Logical Data Design (LDD):** The "Engine & Proof". The authoritative source of truth for all mathematical calculations and validation logic.
5.  **Data Dictionary (DIC):** The "Map". High-fidelity physical source-to-target mapping.
6.  **Lookup Tables (LUT):** The **Universal Translator**. Centralized reference data for categorical labels and hierarchies.

---

### ✈️ Case Study: Grounding the Air Canada AI 

In 2024, an airline chatbot hallucinated a refund policy because it lacked a logic frame. It had empathy, but no grounding. 

**The Solution (Fluent in Human):**
By applying these 5 lines of logic, the AI is forced to follow the business rule instead of its own "feelings."

```json
{
  "MAN": {"Name": "Grounded_Refund_Protocol", "ID": "POL-AIR-004", "Ver": "2.1"},
  "SEM": {"Why": "To ground the AI in factual policy and prevent post-travel liability."},
  "BRG": [{"If": "Post_Travel", "Then": "Deny_Refund", "Why": "Rates must be booked upfront."}],
  "LDD": {"Logic": "IF (Flight_Status == 'Completed') THEN Result = 'Ineligible'"},
  "LUT": {"Policy": "BEREAVE_002", "Action": "Retroactive_Refund", "Allowed": false}
}