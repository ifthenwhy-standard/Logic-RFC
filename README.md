# Structured Logic Disclosure for 2026 Code of Practice
## Project: IfThenWhy™ Logic RFC (v1.0.0)
### NIST-2025-0035 Alignment & Agentic Security Protocol

# IfThenWhy™: The Logic RFC™ (v1.0.0)
## Powered by the Logic DNA™ Architecture
### *Fluent in Human. Designed for AI.*

[![NIST Aligned](https://img.shields.io/badge/NIST-mme--5c57--j61h-blue)](https://www.regulations.gov/comment/NIST-2025-0035)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: USPTO Pending](https://img.shields.io/badge/Trademark-1/10/26-orange)](https://www.uspto.gov)

## A Framework for Deterministic Data Grounding

---

### 🎯 The "IfThenWhy" Mandate
The **IfThenWhy™** framework is a thought leadership model for data architecture that prioritizes **Intent over Infrastructure**. It is built on the belief that data logic must be **Fluent in Human** so that it can be safely **Designed for AI**.

* **The IF (The Trigger):** The business event, user action, or environmental change (The Source of Truth).
* **The THEN (The Data Action):** The mechanical response—the data captured, the row created, or the signal sent.
* **The WHY (The Strategic Intent):** The business purpose, the KPI it feeds, or the human decision it supports. 

> **The IfThenWhy Mandate:** If there is no **Why**, the **Then** shouldn't exist.

---

### 🏛️ Prior Art & Authority
This repository serves as the official machine-readable reference implementation for the **Logic RFC™** framework. It provides the metadata bridge required for AI agents to operate within human-governed business rules.

* **Federal Registry:** Formal submission to NIST completed March 6, 2026 (**mme-5c57-j61h**).
* **Trademark Notice:** "IfThenWhy" and "Logic RFC" are protected marks. USPTO Trademark Application filed: **January 10, 2026**.

---

### 📂 Repository Structure (The Logic DNA™)
This repository is organized as a **Monorepo** to separate the core protocol from its functional implementation.

* **`/spec` (The Protocol):** Contains the core **Logic DNA™** manifests used to achieve **Deterministic Data Grounding** by separating business intent from physical storage:
    * **MAN (Metric Manifest):** The "Master Label"—identifies the Metric Name, ITW ID, Version, and Business Owner.
    * **SEM (Semantic Layer):** The "Business Why"—anchoring metrics to specific Stakeholder Personas.
    * **BRG (Bridge File):** The "If-Then Connector"—the kinetic link between a real-world event and a data action.
    * **LDD (Logical Data Design):** The "Engine & Proof"—the authoritative source for all mathematical calculations.
    * **DIC (Data Dictionary):** The "Map"—the high-fidelity physical source-to-target mapping.
    * **LUT (Lookup Tables):** The "Universal Translator"—centralized reference data for categorical labels.
* **`/app` (The Builder & Auditor):** Contains functional Python tools to automate and secure the framework:
    * **Logic DNA Builder:** Programmatically generates and validates manifests using `openpyxl`.
    * **SQL_Lock.py:** A deterministic logic gate that prevents AI hallucinations and unauthorized logic drift through SHA-256 hash verification.

---

### 🛡️ Functional Governance (`SQL_Lock.py`)
To satisfy **NIST-2025-0035** requirements for continuous monitoring, the `SQL_Lock.py` engine provides:
* **Hallucination Prevention:** Uses SHA-256 Hashing to ensure AI agents only execute human-approved SQL.
* **Daily Heartbeat Patrol:** A "Night Watchman" audit that detects unauthorized intrusions or logic drift within 24 hours.
* **Provenance Ledger:** Maintains a permanent "History Book" of every version, hash, and UAT pass for NIST auditors.
* **Logic Reviewer:** Instantly generates human-readable reports to bridge technical SQL and strategic intent.

---

### 📂 Logic DNA™ Naming Convention
All logic-related files must adhere to the following deterministic naming string to eliminate "Contextual Hallucination":

**`PREFIX_ITW-ID.WHY-ISIC.OWNER.VERSION`**

* **PREFIX**: MAN, SEM, LDD, ERD, DIC, BRG, or LUT.
* **ITW**: Always "ITW" for IfThenWhy assignment.
* **ID**: Unique metric identifier (e.g., 1001).
* **WHY**: Two-digit APQC/PCF process category.
* **ISIC**: One-letter ISIC Section code.
* **OWNER**: Identifies the business owner or organization.

---

### 🤖 Agentic Enforcement (`AGENTS.md`)
AI Agents (Cursor, GitHub Copilot, Claude Code) must read **AGENTS.md** before performing operations. The protocol mandates agents refuse to commit code (The "Then") that lacks a defined "Why" in the SEM or BRG files.

---

### 📜 NIST Standards Citation
To cite the **Logic RFC™** or the **IfThenWhy™** methodology in technical documentation or regulatory filings:

```bibtex
@Manual{ITW_LogicRFC_2026,
  title  = {IfThenWhy: Logic RFC Framework for Deterministic Data Integrity},
  author = {ITW Logic Registry},
  year   = {2026},
  note   = {NIST Public Comment Submission: NIST-2025-0035 (mme-5c57-j61h)},
  url    = {[https://ifthenwhy.ai](https://ifthenwhy.ai)}
}