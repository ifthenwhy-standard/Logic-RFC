import json
import streamlit as st

# --- 4. AUDIT ENGINES (DIOPTRAS & BERT) ---

def calculate_dynamic_robustness(f_path, data):
    """
    DIOPTRAS: Grades the file's robustness based on critical Logic RFC keys.
    Mechanical Integrity check (NIST SP 1270).
    """
    score = 0.75 
    prefix = f_path.stem[:3].upper()
    
    if prefix == "BRG":
        if any(k in data for k in ["Business_Trigger", "if_trigger"]): score += 0.08
        if any(k in data for k in ["Logic_Action", "then_action"]): score += 0.08
        if any(k in data for k in ["Strategic_Intent", "why_intent"]): score += 0.07
    elif prefix == "LDD": 
        if any(k in str(data) for k in ["calculation_logic", "Calculation"]): score += 0.11
        if any(k in str(data) for k in ["validation_logic", "Logic_Action"]): score += 0.12
    elif prefix == "SEM":
        if any(k in data for k in ["Business_Why", "business_why"]): score += 0.11
        if any(k in data for k in ["Strategic_Intent", "strategic_intent"]): score += 0.12
            
    return round(min(score, 1.0), 2)

def audit_bert_faithfulness(metrics_list, paths):
    """
    BERT: Verifying semantic faithfulness using LLM intent alignment.
    Compares the 'Business Why' against the 'Strategic Intent'.
    """
    try:
        from bert_score import score
    except ImportError:
        return [{"ITW_ID": "N/A", "Status": "🚨 ERROR", "Logic": "bert-score library not installed"}]
    
    results = []
    for m in metrics_list:
        # Search for the Semantic Layer file for this ITW_ID
        sem_files = list(paths["spec"].glob(f"**/SEM_{m['itw_id']}*.json"))
        if not sem_files:
            continue
            
        try:
            with open(sem_files[0], 'r', encoding='utf-8') as f:
                data = json.load(f)
                content = data[0] if isinstance(data, list) else data
                
                # Capture the two sides of the 'Why'
                biz = content.get("business_why") or content.get("Business_Why", "")
                strat = content.get("strategic_intent") or content.get("Strategic_Intent", "")
                
                if biz and strat:
                    # BERT Score calculation
                    P, R, F1 = score([biz], [strat], lang="en", verbose=False)
                    f1_val = round(F1.item(), 4)
                    
                    results.append({
                        "ITW_ID": m['itw_id'], 
                        "Score": f1_val, 
                        "Status": "✅ PASS" if f1_val >= 0.85 else "⚠️ REVIEW"
                    })
                else:
                    results.append({
                        "ITW_ID": m['itw_id'], 
                        "Score": 0.0, 
                        "Status": "❌ MISSING DATA"
                    })
        except Exception as e:
            results.append({
                "ITW_ID": m['itw_id'], 
                "Status": "🚨 ERROR", 
                "Logic": str(e)
            })
            
    return results