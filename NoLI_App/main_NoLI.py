import streamlit as st
import streamlit.components.v1 as components
import os
import json
from pathlib import Path
from datetime import datetime
import re

# --- 1. CONFIGURATION & ASSETS ---
LOGO_URL = "https://raw.githubusercontent.com/ifthenwhy-standard/Logic-RFC/main/images%2e/ifthenwhy.svg"
# --- Configuration & Assets ---
BLUEPRINT_ICON = "https://raw.githubusercontent.com/ifthenwhy-standard/Logic-RFC/main/images./blueprint.svg"
BLUEPRINT_URL = "https://raw.githubusercontent.com/ifthenwhy-standard/Logic-RFC/main/images./blueprint.svg"

st.set_page_config(
    page_title="NoLI - IfThenWhy™",
    page_icon="🚨",
    layout="wide"
)

# --- 2. WORKSPACE INITIALIZATION ---
def init_workspace():
    APP_DIR = Path(__file__).resolve().parent
    paths = {
        "templates": APP_DIR.parent / "templates",
        "registry": APP_DIR.parent / "spec" / "registry",
        "output": APP_DIR.parent / "output",
        "spec": APP_DIR.parent / "spec"
    }
    for p in paths.values():
        os.makedirs(p, exist_ok=True)
    return paths

PATHS = init_workspace()

# --- 3. HELPER FUNCTIONS ---
@st.cache_data
def load_json_registry(filename):
    path = PATHS["registry"] / filename
    if not path.exists(): 
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def get_next_available_id(paths):
    used_ids = []
    all_spec_files = list(paths["spec"].glob("**/*.json"))
    for f in all_spec_files:
        match = re.search(r'ITW-(\d{4})', f.name)
        if match:
            used_ids.append(int(match.group(1)))
    return max(used_ids) + 1 if used_ids else 1001

def get_all_spec_files():
    return list(PATHS["spec"].glob("*.json"))

def extract_itw_display_name(filename):
    match = re.search(r'(ITW-\d{4})', filename)
    return match.group(1) if match else filename

def get_registry_data(paths):
    metrics_map = {}
    all_files = list(paths["spec"].glob("*.json"))
    sections = load_json_registry("ISIC_Industry_Section_Codes.json") or []
    section_map = {s.get("ISIC Section"): s.get("Industry Sector Name") for s in sections}

    for f_path in all_files:
        if any(x in str(f_path) for x in ["registry", "templates", "output"]):
            continue
        
        if not (f_path.name.startswith("MAN_") or f_path.name.startswith("SEM_")):
            continue
            
        try:
            parts = f_path.name.split('_')
            if len(parts) < 2: continue
            full_id = parts[1].replace(".json", "")
            
            if full_id not in metrics_map:
                sec_match = re.search(r'-([A-Z])(?:\.|$)', full_id)
                div_match = re.search(r'\.([0-9]{2})(?:\.|$)', full_id)
                sec_letter = sec_match.group(1) if sec_match else "N/A"
                
                metrics_map[full_id] = {
                    "itw_id": full_id, 
                    "category": section_map.get(sec_letter, "General"), 
                    "isic": sec_letter, 
                    "div": div_match.group(1) if div_match else "--",
                    "name": "Unknown", 
                    "details": "No intent recorded"
                }
            
            with open(f_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                content = data[0] if isinstance(data, list) else data
                
                if f_path.name.startswith("MAN_"):
                    name = content.get("metric_name") or content.get("Metric_Name")
                    if name: metrics_map[full_id]["name"] = name
                
                if f_path.name.startswith("SEM_"):
                    details = content.get("business_why") or content.get("Business_Why")
                    if details: metrics_map[full_id]["details"] = details
        except Exception:
            continue
            
    return sorted(metrics_map.values(), key=lambda x: x['itw_id'])

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
    Compares the 'Business Why' against the 'Strategic Intent' to ensure 
    the data action matches the human intent.
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
                    # BERT Score calculation (P=Precision, R=Recall, F1=F-measure)
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

# --- 5. MAIN INTERFACE ---
def main():
    if 'set_created' not in st.session_state:
        st.session_state.set_created = False
        
    with st.sidebar:
        task = st.radio("Select Workflow", [
        "Edit Logic Maps", 
        "Forge (Create)", 
        "View Logic", 
        "Audit (DIOPTRAS)", 
        "Audit (BERT)"])
        st.markdown("---")


        if 'show_info' not in st.session_state:
            st.session_state.show_info = False

        if st.button("ℹ️ Info / Roadmap"):
            st.session_state.show_info = not st.session_state.show_info

        if st.session_state.show_info:
            st.markdown(
                """
                <div style="background-color: #d4edda; color: #155724; padding: 1rem; border-radius: 0.5rem; border: 1px solid #c3e6cb;">
                    <h4 style="display: flex; align-items: center; margin-top: 0;">
                        <img src="{url}" width="25" style="margin-right: 10px;"> 
                        Breathtaking Roadmap
                    </h4>
                    <p style="font-size: 0.85rem;">The NoLI Application Roadmap includes:</p>
                    <ul style="font-size: 0.8rem; margin-top: 0;">
                        <li><strong>Gap Scan:</strong> AI search of news, legal, and regulatory updates to identify conflicts. Review items to <b>add or remove</b> in one click.</li>
                        <li><strong>RAGAS:</strong> Advanced evaluation of RAG faithfulness for Logic Map grounding.</li>
                        <li><strong>Active:</strong> BERT Faithfulness Audits (Live).</li>
                    </ul>
                    <p style="font-size: 0.7rem; opacity: 0.8; margin-top: 10px;">(Click button again to collapse)</p>
                </div>
                """.format(url=BLUEPRINT_URL), 
                unsafe_allow_html=True
            )

        st.markdown("---")
        
        with st.expander("About NoLI & IfThenWhy"):
            st.markdown(
                """
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <img src="{url}" width="60" style="margin-right: 8px;">
                    <strong style="font-size: 1.5rem; line-height: 1; letter-spacing: -0.5px;">IfThenWhy™</strong>
                </div>
                """.format(url=LOGO_URL), 
                unsafe_allow_html=True
            )
            st.markdown("""
            **High-Fidelity Logic Maps for Deterministic Data**
            
            * **Business Leaders:** The "Why" behind the metric.
            * **Technical:** Deterministic source-to-target roadmaps.
            * **Auditors:** Clear business logic audit trails.
            * **AI Agents:** Grounding metadata for authoritative rules.
            """)
















    st.markdown("""
        <style>
            label p { color: #000; font-weight: 500; }
            div.stButton > button:first-child {
                background-color: #0071e3; color: white; border-radius: 20px;
                padding: 10px 40px; min-width: 300px; white-space: nowrap; border: none; font-weight: 600;
            }
            div.stButton > button:contains("Discard/Undo") {
                background-color: #ffffff; color: #d93025; border: 1px solid #d93025;
            }
            .header-label { font-weight: 700; color: #333; font-size: 0.9rem; }
            .itw-wrapper { height: 600px; overflow-y: auto; border: 1px solid #ddd; }
        </style>
    """, unsafe_allow_html=True)
    
    if task == "View Logic":
        st.title("NoLI: Logic Registry")
        metrics = get_registry_data(PATHS)
        
        if not metrics:
            st.warning("No logic maps found. Please forge a new metric manifest.")
        else:
            rows = "".join([f"<tr><td>»</td><td>{m['itw_id']}</td><td>{m['category']}</td><td>{m['isic']}</td><td>{m['div']}</td><td>{m['name']}</td><td>{m['details']}</td></tr>" for m in metrics])
            
            registry_html = f"""
            <div class="itw-wrapper">
                <style>
                    table {{ width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 11px; }}
                    th {{ background: #f4f4f4; padding: 12px; border-bottom: 2px solid #333; position: sticky; top: 0; text-align: left; }}
                    td {{ padding: 10px; border-bottom: 1px solid #eee; }}
                    tr:hover {{ background: #f9f9f9; }}
                </style>
                <table>
                    <thead>
                        <tr><th>Link</th><th>ITW_ID</th><th>Persona</th><th>ISIC</th><th>Div</th><th>Metric_Name</th><th>Intent Details</th></tr>
                    </thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
            """
            components.html(registry_html, height=650, scrolling=True)


    elif task == "Edit Logic Maps":
        st.title("Logic Map Files")
        st.header("Edit Logic Maps")
        spec_files = get_all_spec_files()
        
        if not spec_files:
            st.warning("No logic maps found in the /spec directory.")
        else:
            # Re-establishing the map between display name and actual file path
            file_map = {extract_itw_display_name(f.name): f for f in spec_files}
            selected_itw = st.selectbox("Select ITW_ID", options=[""] + sorted(list(file_map.keys())))
            
            if selected_itw:
                target_path = file_map[selected_itw]
                with open(target_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except Exception as e:
                        st.error(f"Error reading logic file: {e}")
                        data = {}
                
                # Handling both list-wrapped and direct dictionary JSONs
                content = data[0] if isinstance(data, list) else data
                updated_content = {}
                
                h1, h2 = st.columns([2, 5])
                with h1: st.markdown('<p class="header-label">Framework Field</p>', unsafe_allow_html=True)
                with h2: st.markdown('<p class="header-label">Deterministic Value</p>', unsafe_allow_html=True)

                for k, v in content.items():
                    c1, c2 = st.columns([2, 5])
                    with c1: 
                        # Fields are rendered but keys are disabled to protect the schema
                        st.text_input("K", value=k, disabled=True, key=f"k_{selected_itw}_{k}", label_visibility="collapsed")
                    with c2: 
                        # Protect core protocol fields from accidental editing
                        is_prot = k.lower() in ["itw_id", "version", "original_author", "file_type"]
                        updated_content[k] = st.text_input("V", value=str(v), disabled=is_prot, key=f"v_{selected_itw}_{k}", label_visibility="collapsed")
                
                if st.button("Save Changes"):
                    # Update the audit timestamp for DIOPTRAS tracking
                    updated_content["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(target_path, "w", encoding="utf-8") as f:
                        json.dump(updated_content, f, indent=4)
                    st.success(f"Logic for {selected_itw} Synchronized.")
                    st.rerun()





    elif task == "Forge (Create)":
        st.title("Logic Map Files")
        st.header("Forge New Metric")
        
        sections = load_json_registry("ISIC_Industry_Section_Codes.json") or [{"Industry Sector Name": "General", "ISIC Section": "Z"}]
        divisions = load_json_registry("ISIC_Industry_Division_Codes.json") or []
        pcf_cats = load_json_registry("PCF_Categories.json") or [{"PCF Category": "Generic", "PCF Code": "0.0"}]
        
        col_name, col_id = st.columns([3, 1])
        with col_name: logic_map_name = st.text_input("Metric Name (Logic Label)")
        with col_id: unique_id = st.text_input("ID", value=str(get_next_available_id(PATHS)))

        section = st.selectbox("Industry Section", sections, format_func=lambda x: x.get("Industry Sector Name"))
        sec_letter = section.get("ISIC Section", "Z")
        
        filtered_divs = [d for d in divisions if d.get("ISIC Section") == sec_letter] or [{"Industry Sector / Activity Name": "Default", "ISIC Division": "00"}]
        division = st.selectbox("Industry Division", filtered_divs, format_func=lambda x: x.get("Industry Sector / Activity Name"))
        pcf = st.selectbox("PCF Category", pcf_cats, format_func=lambda x: x.get("PCF Category"))
        
        pcf_code = str(pcf.get('PCF Code')).split('.')[-1].zfill(2)
        div_code = re.sub(r'\D', '', str(division.get('ISIC Division')))[-3:].zfill(3)
        full_itw_id = f"ITW-{unique_id}.{pcf_code}-{sec_letter}.{div_code}.REF.001"
        
        st.info(f"**Target ITW_ID:** `{full_itw_id}`")

        c1, c2, _ = st.columns([3, 3, 2])
        with c1:
            if st.button("Generate Logic Set"):
                man_content = {
                    "itw_id": full_itw_id, 
                    "metric_name": logic_map_name, 
                    "version": "001",
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                file_path = PATHS["spec"] / f"MAN_{full_itw_id}.json"
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(man_content, f, indent=4)
                st.session_state.last_path = str(file_path)
                st.session_state.set_created = True
                st.success(f"Generated {file_path.name}")
        with c2:
            if st.session_state.set_created:
                if st.button("Discard/Undo"):
                    if os.path.exists(st.session_state.last_path): os.remove(st.session_state.last_path)
                    st.session_state.set_created = False
                    st.rerun()

    elif task == "Audit (DIOPTRAS)":
        st.title("DIOPTRAS | Logic Robustness Audit")
        st.subheader("NIST SP 1270: Mechanical Transparency Check")
        if st.button("Execute DIOPTRAS Audit"):
            results = []
            metrics = get_registry_data(PATHS)
            for m in metrics:
                for f_path in PATHS["spec"].glob(f"*{m['itw_id']}*.json"):
                    try:
                        with open(f_path, 'r') as f:
                            data = json.load(f)
                        score = calculate_dynamic_robustness(f_path, data)
                        results.append({
                            "ITW_ID": m['itw_id'], "File": f_path.name,
                            "Score": score, "Status": "✅ PASS" if score >= 0.90 else "⚠️ INCOMPLETE"
                        })
                    except: continue
            if results: st.table(results)
            else: st.info("No files found for mechanical audit.")

    elif task == "Audit (BERT)":
        st.title("BERT | Semantic Faithfulness Audit")
        st.subheader("Standard: AI Intent Alignment")
        
        # 1. Grab the data first to verify it exists
        metrics_to_audit = get_registry_data(PATHS)
        
        if not metrics_to_audit:
            st.warning("No metrics found in registry. Audit cannot proceed.")
        else:
            st.info(f"Found {len(metrics_to_audit)} metrics available for audit.")
            
            # 2. The Button trigger
            if st.button("Run BERT Audit Engine"):
                with st.spinner("Calculating Semantic Alignment..."):
                    results = audit_bert_faithfulness(metrics_to_audit, PATHS)
                
                # 3. Explicitly check results
                if results:
                    st.table(results)
                else:
                    st.error("Audit returned no results. Check if SEM files exist in /spec.")

# --- 6. LOGIC RFC ARCHITECTURE HANDLERS ---
def check_ldd_logic():
    """Future: Validates LDD calculation proof."""
    return True

def check_dic_mapping():
    """Future: Validates Dictionary source-to-target mapping."""
    return True

def check_lut_reference():
    """Future: Validates Lookup Table categorical consistency."""
    return True

if __name__ == "__main__":
    main()