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
The Logic RFC uses a 6-file architecture to ensure that every data action taken by an AI agent is authorized, audited, and mathematically verified.

1.  **Metric Manifest (MAN):** The "Master Label" and **Identity Anchor**. It defines the ITW_ID and Version, acting as the unique identifier for agentic identity and authorization.
2.  **Semantic Layer (SEM):** The "Business Why". Natural language manifests that anchor every metric to a specific Stakeholder Persona.
3.  **Bridge File (BRG):** The **Kinetic Link**. Maps the business trigger (If) to the data action (Then). This is the primary control for preventing hallucinations.
4.  **Logical Data Design (LDD):** The "Engine & Proof". The authoritative source of truth for all mathematical calculations, providing the deterministic grounding required by NIST AI 800-2.
5.  **Data Dictionary (DIC):** The "Map". High-fidelity physical source-to-target mapping.
6.  **Lookup Tables (LUT):** The **Universal Translator**. Centralized reference data for all categorical labels and hierarchies.

---

### 🛡️ SQL_Lock: The 5-Second Audit Protocol
This repository includes a reference Python implementation that acts as a **Digital Deadbolt** for SQL execution. It verifies **BRG** authorization and validates math against the **LDD** to ensure **Non-Repudiation**—addressing the core security concerns of the April 2nd NIST Concept Paper.

---

### ⚖️ Legal & Trademark Notice

**1. Software License:**
The technical logic, file schemas, and reference code in this repository are licensed under the **Apache License, Version 2.0** (the "License"). You may obtain a copy of the License at [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0).

**2. Attribution & Notice:**
Per Section 4(d) of the Apache 2.0 License, **attribution must be maintained** as specified in the [NOTICE](NOTICE) file located in the root directory of this repository. Any redistribution of this work or derivative