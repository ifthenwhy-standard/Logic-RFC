import streamlit as st
import streamlit.components.v1 as components
import os
import json
from pathlib import Path
from datetime import datetime
import re

# --- 1. CONFIGURATION & ASSETS ---
BLUEPRINT_URL = "https://raw.githubusercontent.com/ifthenwhy-standard/Logic-RFC/main/images%2e/blueprint.svg"
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
    os.makedirs(paths["output"], exist_ok=True)
    return paths

PATHS = init_workspace()

# --- 3. HELPER FUNCTIONS ---
@st.cache_data
def load_json_registry(filename):
    path = PATHS["registry"] / filename
    if not path.exists(): 
        return None
    with open(path, 'r') as f: 
        return json.load(f)

def get_next_available_id(paths):
    used_ids = []
    all_spec_files = list(paths["spec"].glob("**/*.json"))
    for f in all_spec_files:
        match = re.search(r'ITW-(\d{4})', f.name)
        if match:
            used_ids.append(int(match.group(1)))
    return max(used_ids) + 1 if used_ids else 1000

def get_registry_data(paths):
    metrics_map = {}
    all_files = list(paths["spec"].glob("**/*.json"))
    sections = load_json_registry("ISIC_Industry_Section_Codes.json") or []
    section_map = {s.get("ISIC Section"): s.get("Industry Sector Name") for s in sections}

    for f_path in all_files:
        if "registry" in str(f_path) or "templates" in str(f_path): continue
        if not (f_path.name.startswith("MAN_") or f_path.name.startswith("SEM_")): continue
        try:
            full_id = f_path.name.split('_')[1].replace(".json", "")
            if full_id not in metrics_map:
                sec_match = re.search(r'-([A-Z])(?:\.|$)', full_id)
                sec_letter = sec_match.group(1) if sec_match else "N/A"
                div_match = re.search(r'\.([0-9]{2})(?:\.|$)', full_id)
                div_code = div_match.group(1) if div_match else "--"
                isic_name = section_map.get(sec_letter, "General")
                metrics_map[full_id] = {
                    "itw_id": full_id,
                    "id_prefix": full_id.split('.')[0],
                    "id_suffix": ".".join(full_id.split('.')[1:]),
                    "category": isic_name, 
                    "isic": sec_letter,
                    "div": div_code,
                    "name": "", 
                    "details": ""
                }
            with open(f_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle cases where data might be a list or a dict
                content = data[0] if isinstance(data, list) else data
                
                if f_path.name.startswith("MAN_"):
                    metrics_map[full_id]["name"] = content.get("Metric_Name", content.get("metric_name", ""))
                
                if f_path.name.startswith("SEM_"):
                    # Robust check for the description field to prevent blank cells
                    details = content.get("Business_Why") or content.get("business_why") or content.get("Strategic_Intent") or ""
                    metrics_map[full_id]["details"] = details
                    
                    persona = content.get("Stakeholder_Persona") or content.get("stakeholder_persona")
                    if persona:
                        metrics_map[full_id]["category"] = persona
        except Exception: continue
    return sorted(metrics_map.values(), key=lambda x: x['itw_id'])

def audit_bert_faithfulness(metrics_list, paths):
    from bert_score import score
    results = []
    for m in metrics_list:
        sem_files = list(paths["spec"].glob(f"**/SEM_{m['itw_id']}*.json"))
        if not sem_files: continue
        try:
            with open(sem_files[0], 'r', encoding='utf-8') as f:
                data = json.load(f)
                sem_data = data[0] if isinstance(data, list) else data
                biz_why = sem_data.get("Business_Why", sem_data.get("business_why", ""))
                strat_intent = sem_data.get("Strategic_Intent", sem_data.get("strategic_intent", ""))
                if biz_why and strat_intent:
                    P, R, F1 = score([biz_why], [strat_intent], lang="en", verbose=False)
                    f1_val = round(F1.item(), 4)
                    status = "✅ PASS" if f1_val >= 0.85 else "⚠️ REVIEW"
                    results.append({"ITW_ID": m['itw_id'], "Score": f1_val, "Status": status, "Logic": "BERT Faithfulness"})
                else:
                    results.append({"ITW_ID": m['itw_id'], "Score": 0.0, "Status": "❓ SKIP", "Logic": "Missing Intent/Why"})
        except Exception as e:
            results.append({"ITW_ID": m['itw_id'], "Score": 0.0, "Status": "🚨 ERROR", "Logic": str(e)})
    return results

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    task = st.radio("Select Workflow", ["Forge (Edit)", "View Logic", "Audit (Test)"])
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

# --- 5. MAIN INTERFACE ---
def main():
    if task == "Forge (Edit)":
        st.title("Logic Map Files")
        st.header("Edit")
        
        sections = load_json_registry("ISIC_Industry_Section_Codes.json")
        divisions = load_json_registry("ISIC_Industry_Division_Codes.json")
        pcf_cats = load_json_registry("PCF_Categories.json")

        if not all([sections, divisions, pcf_cats]):
            st.error("Missing Registry files in /spec/registry.")
            return

        col1, col2 = st.columns(2)
        with col1:
            next_id = str(get_next_available_id(PATHS))
            unique_id = st.text_input("4-Digit Metric ID", value=next_id, max_chars=4)
        with col2:
            metric_name = st.text_input("Metric Name")

        section = st.selectbox("Industry Section", sections, format_func=lambda x: x["Industry Sector Name"])
        sec_letter = section.get("ISIC Section")

        filtered_divs = [d for d in divisions if d.get("ISIC Section") == sec_letter]
        division = st.selectbox("Industry Division", filtered_divs, format_func=lambda x: x["Industry Sector / Activity Name"])

        pcf = st.selectbox("PCF Category", pcf_cats, format_func=lambda x: f"{x['PCF Code']} - {x['PCF Category']}")
        corp_id = st.text_input("Status/Company ID", value="REF").upper()
        ver_num = st.text_input("Version", value="001")

        pcf_val = str(pcf['PCF Code']).split('.')[-1].zfill(2)
        div_clean = re.sub(r'\D', '', str(division['ISIC Division']))[-3:].zfill(3)
        full_itw_id = f"ITW-{unique_id}.{pcf_val}-{sec_letter}.{div_clean}.{corp_id}.{ver_num}"

        st.info(f"**Target ITW_ID:** &nbsp;&nbsp; `{full_itw_id}`")

    elif task == "View Logic":
        st.title(f"NoLI: {task}")
        metrics_list = get_registry_data(PATHS)
        rows_html = ""
        for m in metrics_list:
            highlight = 'class="highlight-blue"' if "1002" in m['itw_id'] else ""
            rows_html += f"""
            <tr {highlight}>
              <td><a href="#" class="chevron-link">»</a></td>
              <td class="itw-id-cell"><span class="id-prefix">{m['id_prefix']}</span>.{m['id_suffix']}</td>
              <td>{m['category']}</td>
              <td>{m['isic']}</td>
              <td>{m['div']}</td>
              <td>{m['name']}</td>
              <td>{m['details']}</td>
            </tr>"""

        full_html = f"""
        <style>
          #itw-table-wrapper {{ margin-top: 10px; border: 1px solid #ddd; background-color: #fff; padding: 8px; font-family: sans-serif; }}
          #metricSearchInput {{ width: 100%; padding: 6px; margin-bottom: 8px; border: 1px solid #ccc; border-radius: 4px; }}
          .itw-scroll-container {{ overflow-y: auto; max-height: 550px; }}
          #myMetricTable {{ width: 100%; border-collapse: collapse; font-size: 11px; }}
          .metric-list-title {{ background-color: #e2e8f0; font-weight: 800; text-align: center; padding: 8px; font-size: 14px; text-transform: uppercase; }}
          #myMetricTable th {{ position: sticky; top: 0; background: #f4f4f4; padding: 6px 8px; border-bottom: 2px solid #333; }}
          #myMetricTable td {{ padding: 6px 8px; border-bottom: 1px solid #eee; }}
          .id-prefix {{ color: #000080; font-weight: 800; display: block; }}
          .highlight-blue {{ background-color: #e0f2fe !important; border-left: 4px solid #2563eb; }}
          .chevron-link {{ text-decoration: none; color: #2563eb; font-weight: bold; }}
        </style>
        <div id="itw-table-wrapper">
          <input type="text" id="metricSearchInput" onkeyup="searchTable()" placeholder="Search registry...">
          <div class="itw-scroll-container">
            <table id="myMetricTable">
              <thead>
                <tr><th colspan="7" class="metric-list-title">Logic RFC™ Registry</th></tr>
                <tr><th>Link</th><th>ITW_ID</th><th>Category</th><th>ISIC</th><th>Div</th><th>Description</th><th>Details</th></tr>
              </thead>
              <tbody>{rows_html}</tbody>
            </table>
          </div>
        </div>
        <script>
          function searchTable() {{
            var input = document.getElementById("metricSearchInput");
            var filter = input.value.toUpperCase();
            var tr = document.getElementById("myMetricTable").getElementsByTagName("tr");
            for (var i = 2; i < tr.length; i++) {{
              var txt = tr[i].innerText.toUpperCase();
              tr[i].style.display = txt.indexOf(filter) > -1 ? "" : "none";
            }}
          }}
        </script>"""
        components.html(full_html, height=750, scrolling=True)

    elif task == "Audit (Test)":
        st.title("Audit (Test)")
        st.markdown("### Logic RFC™ Governance")
        st.info("Logic: BERT compares the *Business_Why* (Strategic Purpose) to the *Strategic_Intent* (The Goal).")
        st.caption("Protocol: Scores below 85% (0.85) require Human-in-the-Loop validation.")

        if st.button("Execute BERT Faithfulness Audit"):
            metrics = get_registry_data(PATHS)
            with st.spinner("Analyzing semantic similarity via BERT..."):
                audit_data = audit_bert_faithfulness(metrics, PATHS)
                if audit_data:
                    st.table(audit_data)
                    st.success("Audit complete. Please review any '⚠️ REVIEW' flags.")
                else:
                    st.warning("No SEM files found in /spec to audit.")

        st.markdown("---")
        st.write("### Roadmap")
        st.write("• RAGAS Relevancy (Coming Soon)")
        st.write("• SQL Determinism (Coming Soon)")

if __name__ == "__main__":
    main()