import streamlit as st
import streamlit.components.v1 as components
import os
import json
from pathlib import Path
from datetime import datetime
import re

# --- 1. CONFIGURATION & ASSETS ---
LOGO_URL = "https://raw.githubusercontent.com/ifthenwhy-standard/Logic-RFC/main/images%2e/ifthenwhy.svg"

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
                    details = content.get("business_why") or content.get("Business_Why") or content.get("strategic_intent")
                    if details: metrics_map[full_id]["details"] = details
                    persona = content.get("stakeholder_persona") or content.get("Stakeholder_Persona")
                    if persona: metrics_map[full_id]["category"] = persona
        except Exception:
            continue
            
    return sorted(metrics_map.values(), key=lambda x: x['itw_id'])

# --- 4. AUDIT & LOGIC TESTING ---
def audit_bert_faithfulness(metrics_list, paths):
    try:
        from bert_score import score
    except ImportError:
        return [{"Error": "bert-score library not installed"}]
    
    results = []
    for m in metrics_list:
        sem_files = list(paths["spec"].glob(f"**/SEM_{m['itw_id']}*.json"))
        if not sem_files: continue
        try:
            with open(sem_files[0], 'r', encoding='utf-8') as f:
                data = json.load(f)
                content = data[0] if isinstance(data, list) else data
                biz = content.get("business_why") or content.get("Business_Why", "")
                strat = content.get("strategic_intent") or content.get("Strategic_Intent", "")
                
                if biz and strat:
                    P, R, F1 = score([biz], [strat], lang="en", verbose=False)
                    f1_val = round(F1.item(), 4)
                    results.append({
                        "ITW_ID": m['itw_id'], 
                        "Score": f1_val, 
                        "Status": "✅ PASS" if f1_val >= 0.85 else "⚠️ REVIEW"
                    })
        except Exception as e:
            results.append({"ITW_ID": m['itw_id'], "Status": "🚨 ERROR", "Logic": str(e)})
    return results

# --- 5. MAIN INTERFACE ---
def main():
    if 'set_created' not in st.session_state:
        st.session_state.set_created = False
        
    with st.sidebar:
        task = st.radio("Select Workflow", ["Edit Logic Maps", "Forge (Create)", "View Logic", "Audit (Test)"])
        st.markdown("---")
        with st.expander("About NoLI"):
            st.markdown(f'<img src="{LOGO_URL}" width="60"> **IfThenWhy™**', unsafe_allow_html=True)
            st.caption("Standardizing intent over infrastructure.")

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

    if task == "Edit Logic Maps":
        st.title("Logic Map Files")
        st.header("Edit Logic Maps")
        spec_files = get_all_spec_files()
        
        if not spec_files:
            st.warning("No logic maps found in the /spec directory.")
        else:
            file_map = {extract_itw_display_name(f.name): f for f in spec_files}
            selected_itw = st.selectbox("Select ITW_ID", options=[""] + sorted(list(file_map.keys())))
            
            if selected_itw:
                with open(file_map[selected_itw], "r", encoding="utf-8") as f:
                    data = json.load(f)
                content = data[0] if isinstance(data, list) else data
                updated_content = {}
                
                h1, h2 = st.columns([2, 5])
                with h1: st.markdown('<p class="header-label">Framework Field</p>', unsafe_allow_html=True)
                with h2: st.markdown('<p class="header-label">Deterministic Value</p>', unsafe_allow_html=True)

                for k, v in content.items():
                    c1, c2 = st.columns([2, 5])
                    with c1: st.text_input("K", value=k, disabled=True, key=f"k_{k}", label_visibility="collapsed")
                    with c2: 
                        is_prot = k.lower() in ["itw_id", "version", "original_author"]
                        updated_content[k] = st.text_input("V", value=str(v), disabled=is_prot, key=f"v_{k}", label_visibility="collapsed")
                
                if st.button("Save Changes"):
                    updated_content["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(file_map[selected_itw], "w", encoding="utf-8") as f:
                        json.dump(updated_content, f, indent=4)
                    st.success("Logic Synchronized.")

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
                    if os.path.exists(st.session_state.last_path):
                        os.remove(st.session_state.last_path)
                    st.session_state.set_created = False
                    st.warning("Action Undone.")
                    st.rerun()

    elif task == "View Logic":
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

    elif task == "Audit (Test)":
        st.title("Logic Intent Audit")
        st.write("Verifying semantic faithfulness using BERT Score.")
        if st.button("Run Audit"):
            results = audit_bert_faithfulness(get_registry_data(PATHS), PATHS)
            if results: 
                st.table(results)
            else: 
                st.info("No semantic layers (SEM) found for analysis.")

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