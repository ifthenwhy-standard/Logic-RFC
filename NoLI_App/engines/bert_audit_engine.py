import streamlit as st
import json
from datetime import datetime

def run_bert_audit_workflow(PATHS, get_registry_data, load_json_registry):
    """
    BERT Engine: Verifying semantic faithfulness.
    Combines the heavy math of bert-score with the NoLI UI.
    """
    st.title("BERT | Semantic Faithfulness Audit")
    st.subheader("Measuring Intent Alignment (Business Why vs. Strategic Intent)")

    if st.button("Execute BERT Semantic Audit"):
        # 1. Attempt the heavy-duty import locally to avoid crashing the whole app
        try:
            from bert_score import score
        except ImportError:
            st.error("🚨 ERROR: `bert-score` library not installed. Run: pip install bert-score")
            return

        results = []
        metrics = get_registry_data(PATHS, load_json_registry)
        
        with st.spinner("Calculating Semantic Similarity..."):
            for m in metrics:
                # Search for the Semantic Layer (SEM) file
                sem_files = list(PATHS["spec"].glob(f"**/SEM_{m['itw_id']}*.json"))
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
                            # The Real Logic: P=Precision, R=Recall, F1=F-measure
                            P, R, F1 = score([biz], [strat], lang="en", verbose=False)
                            f1_val = round(F1.item(), 4)
                            
                            results.append({
                                "ITW_ID": m['itw_id'], 
                                "F1-Score": f1_val, 
                                "Status": "✅ PASS" if f1_val >= 0.85 else "⚠️ REVIEW"
                            })
                        else:
                            results.append({
                                "ITW_ID": m['itw_id'], 
                                "F1-Score": 0.0, 
                                "Status": "❌ MISSING DATA"
                            })
                except Exception as e:
                    results.append({"ITW_ID": m['itw_id'], "Status": "🚨 ERROR", "Logic": str(e)})

        if results:
            st.table(results)
        else:
            st.info("No SEM files found for audit.")