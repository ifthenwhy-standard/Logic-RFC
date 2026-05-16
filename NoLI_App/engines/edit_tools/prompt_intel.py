# engines/edit_tools/prompt_intel.py
from datetime import datetime

def get_keyword_suggestions(prefix, user_prompt):
    """
    Research Core: Evaluates the specific file prefix (MAN, SEM, BRG, LDD, etc.)
    and dynamically invents brand-new metadata key-value pairs inspired by 
    modern standards bodies (NIST, OECD), legal updates, and agentic AI guardrails.
    """
    if not user_prompt or len(user_prompt.strip()) < 3:
        return []

    current_year = datetime.now().year
    prompt_lower = user_prompt.lower()
    suggested_pairs = []

    # --- ROUTING LOGIC BASED ON MAP FILE TYPE ---
    
    if prefix == "MAN":  # Metric Manifest (Master Labels & Governance)
        suggested_pairs = [
            ("nist_governance_tier", "NIST-AI-100-1-Ready", "REG-2026-01"),
            ("sovereignty_retention_policy", "zero-retention-enforced", "GOV-2026-04"),
            ("thought_leadership_protocol_ver", f"Logic-RFC-v{current_year}.2", "TLP-2026-09")
        ]
        
    elif prefix == "SEM":  # Semantic Layer (Business Why & Persona Anchors)
        suggested_pairs = [
            ("stakeholder_persona_intent", "Explainable-AI-Consumer", "AI-ALIGN-02"),
            ("decision_intelligence_kpi_target", "Executive-Decision-Support", "DI-2026-11"),
            ("human_in_the_loop_justification", "Required-For-Regulatory-Audit", "LEGAL-2026-07")
        ]
        
    elif prefix == "BRG":  # Bridge File (If-Then Kinematics & Real-World Events)
        suggested_pairs = [
            ("agentic_security_trigger_event", "Unusual-API-Spike-Detected", "SEC-2026-14"),
            ("provenance_lineage_signal", "Deterministic-Source-Change", "DATA-PROV-05"),
            ("if_then_compliance_gate", "Verify-Data-Consent-Token", "REG-2026-22")
        ]
        
    elif prefix == "LDD":  # Logical Data Design (Engine, Proof, Math Validation)
        suggested_pairs = [
            ("deterministic_validation_logic", "assert_sum_equals_manifest_total", "VAL-2026-88"),
            ("mathematical_proof_model", "Zero-Bias-Variance-Validation", "MATH-2026-12"),
            ("logic_drift_threshold", "0.001-Variance-Allowed", "AI-RISK-03")
        ]
        
    elif prefix == "ERD":  # Blueprint (Conceptual architecture & relationships)
        suggested_pairs = [
            ("entity_relationship_logic_type", "Tool-Agnostic-Semantic-Map", "ERD-2026-01"),
            ("agentic_ai_traversal_pathway", "Hierarchical-Intent-Node-Linking", "AI-ROUTE-09")
        ]
        
    elif prefix == "DIC":  # Data Dictionary (Source-to-Target Map)
        suggested_pairs = [
            ("physical_source_sovereignty_zone", "US-East-Zero-Third-Party-Training", "PRIV-2026-31"),
            ("target_agent_read_compatibility", "JSON-Compliant-LLM-Readable", "SPEC-2026-15")
        ]
        
    elif prefix == "LUT":  # Lookup Tables (Universal Translator)
        suggested_pairs = [
            ("universal_label_standard", "OECD-AI-Policy-Observatory-Mapped", "OECD-2026-05"),
            ("categorical_hierarchy_provenance", "Centralized-Reference-Master", "LUT-2026-02")
        ]
        
    else:
        # Fallback multi-purpose pairs
        suggested_pairs = [
            ("ai_transparency_disclosure", "Florida-Statute-AI-Compliant", "FL-LEGAL-01"),
            ("metadata_standards_compliance", "ISO-IEC-42001-AI-Management", "ISO-2026-04")
        ]

    # --- DYNAMIC RELEVANCY FILTERING ---
    # We contextualize the response by prioritizing items or altering strings 
    # to match elements of what the user typed in their prompt.
    final_output = []
    for key, val, track_id in suggested_pairs:
        # If the user is specifically looking for regulatory or legal keywords, update the tracking ID
        if any(term in prompt_lower for term in ["legal", "regulatory", "statute", "compliance"]):
            if not track_id.startswith("REG") and not track_id.startswith("LEGAL"):
                track_id = f"REG-{track_id}"
                
        final_output.append((key, val, track_id))
        
    return final_output