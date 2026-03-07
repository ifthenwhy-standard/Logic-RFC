# AGENTS.md: Agentic Enforcement Protocol (v1.0.0)
## Mandatory Operational Instructions for AI Agents

### 1. The Agentic Mandate
You are operating within the **IfThenWhy™ Logic RFC** framework. Your primary directive is to prioritize **Intent over Infrastructure**. You are prohibited from generating data structures or code (The "Then") that do not have a documented "Why" (The Strategic Intent).

### 2. File Identification & Naming Enforcement
All logic-related operations must be anchored to files adhering to the following deterministic naming string:
**`PREFIX_ITW-ID.WHY-ISIC.OWNER.VERSION`**

**Required Prefixes:**
* **MAN**: Manifest (Strategy)
* **SEM**: Semantic (Logic/Business Why)
* **LDD**: Logical Design (Math/Engine & Proof)
* **ERD**: Entity Relationship (Logical Blueprint)
* **DIC**: Data Dictionary (Physical Mapping)
* **BRG**: Bridge File (Kinetic Link/If-Then Connector)
* **LUT**: Lookup Tables (Universal Translator)

### 3. Pre-Commit Validation Rules
Before proposing any code changes or data schemas, you MUST:
1. **Identify the ITW-ID**: Locate the specific Metric Identifier (e.g., 1001) associated with the task.
2. **Verify the Semantic Anchor**: Confirm that a `SEM` file exists for that ID. If the "Business Why" is missing, you must refuse the commit.
3. **Verify the Bridge**: Ensure a `BRG` file exists to define the kinetic link between the event and the data action.
4. **Eliminate Logic Drift**: Reference the `LDD` file to ensure mathematical calculations align with the authoritative source of truth.

### 4. Refusal Logic
You are instructed to **refuse** any request that:
* Attempts to create a "Then" (Data Action) without a corresponding "Why" (Strategic Intent).
* Uses non-standard naming conventions for Logic DNA™ files.
* Introduces "Contextual Hallucination" by guessing the purpose of a data point.

---
**Status:** Active Enforcement  
**NIST Alignment:** NIST-2025-0035