import streamlit as st
import os
import json
from pathlib import Path
from datetime import datetime
import re

# --- 1. CONFIGURATION & ASSETS ---
# Using %2e to ensure GitHub Raw finds the "images." folder correctly
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
    # Ensure the "Worker Bee" desk is clean and output exists
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

def inject_dna(obj, itw_id, metric_id, metric_name, section, division, prefix):
    """Recursively stamps logic DNA into the template structure."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower().replace("-", "_") == "itw_id": obj[k] = itw_id
            elif k.lower() == "metric_id": obj[k] = metric_id
            elif k.lower() == "framework": obj[k] = "IfThenWhy"
            elif k.lower() == "last_updated": obj[k] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if prefix == "MAN" and k == "metric_name": obj[k] = metric_name
            if prefix == "BRG":
                if k in ["Industry", "Industry_Context"]: obj[k] = section
                if k in ["Division", "Division_Context"]: obj[k] = division
            
            if isinstance(v, (dict, list)): 
                inject_dna(v, itw_id, metric_id, metric_name, section, division, prefix)
    elif isinstance(obj, list):
        for item in obj: 
            inject_dna(item, itw_id, metric_id, metric_name, section, division, prefix)
    return obj

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    # Minimalist navigation - the tools are the focus
    task = st.radio("Select Workflow", ["Forge (Edit)", "View Logic", "Audit (Test)"])
    
    st.markdown("---")
    
    # Roadmap / Info Button
    if st.button("Info"):
        st.markdown(
            """
            <div style="background-color: #d4edda; color: #155724; padding: 1rem; border-radius: 0.5rem; border: 1px solid #c3e6cb;">
                <h4 style="display: flex; align-items: center; margin-top: 0;">
                    <img src="{url}" width="25" style="margin-right: 10px;"> 
                    Coming Soon!
                </h4>
                <p style="font-size: 0.85rem;">The NoLI Application Roadmap includes:</p>
                <ul style="font-size: 0.8rem; margin-top: 0;">
                    <li><strong>Create/Edit:</strong> Repo updates.</li>
                    <li><strong>Convert:</strong> SQL to Logic RFC.</li>
                    <li><strong>Audit:</strong> High-fidelity reports.</li>
                    <li><strong>Validation:</strong> RAGAS & BERT.</li>
                </ul>
            </div>
            """.format(url=BLUEPRINT_URL), 
            unsafe_allow_html=True
        )

    st.markdown("---")
    
    # Branded About Section
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
    # Dynamic Title Logic
    if task == "Forge (Edit)":
        display_title = "Logic Map Files"
    else:
        display_title = f"NoLI: {task}"

    st.title(display_title)

    if task == "Forge (Edit)":
        st.header("Edit")
        
        # Load Registry Files
        sections = load_json_registry("ISIC_Industry_Section_Codes.json")
        divisions = load_json_registry("ISIC_Industry_Division_Codes.json")
        pcf_cats = load_json_registry("PCF_Categories.json")

        if not all([sections, divisions, pcf_cats]):
            st.error("Missing Registry files in /spec/registry. Please check your folder structure.")
            return

        # UI Input Fields
        col1, col2 = st.columns(2)
        with col1:
            unique_id = st.text_input("4-Digit Metric ID", value="1000", max_chars=4)
        with col2:
            metric_name = st.text_input("Metric Name")

        # Dynamic Dropdowns
        section = st.selectbox("Industry Section", sections, format_func=lambda x: x["Industry Sector Name"])
        sec_letter = section.get("ISIC Section")

        filtered_divs = [d for d in divisions if d.get("ISIC Section") == sec_letter]
        division = st.selectbox("Industry Division", filtered_divs, format_func=lambda x: x["Industry Sector / Activity Name"])
        
        pcf = st.selectbox("PCF Category", pcf_cats, format_func=lambda x: f"{x['PCF Code']} - {x['PCF Category']}")

        corp_id = st.text_input("Status/Company ID", value="EXP").upper()
        ver_num = st.text_input("Version", value="001")

        # ITW_ID Generation
        pcf_val = str(pcf['PCF Code']).split('.')[-1].zfill(2)
        div_clean = re.sub(r'\D', '', str(division['ISIC Division']))[-3:].zfill(3)
        full_itw_id = f"itw_{unique_id}.{pcf_val}.{sec_letter}.{div_clean}.{corp_id}.{ver_num}"
        
        st.info(f"**ITW_ID:** &nbsp;&nbsp; `{full_itw_id}`")

        if st.button("Create"):
            templates = list(PATHS["templates"].glob("*.json"))
            
            if not templates:
                st.warning("No templates found in /templates.")
                return

            for t_path in templates:
                with open(t_path, 'r') as f:
                    template_data = json.load(f)
                
                prefix = t_path.name.split('_')[0]
                new_filename = f"{prefix}_ITW-{unique_id}.{pcf_val}-{sec_letter}.{div_clean}.{corp_id}.{ver_num}.json"
                
                stamped_content = inject_dna(
                    template_data, 
                    full_itw_id, 
                    f"itw_{unique_id}", 
                    metric_name, 
                    section["Industry Sector Name"], 
                    division["Industry Sector / Activity Name"], 
                    prefix
                )
                
                with open(PATHS["output"] / new_filename, 'w') as f:
                    json.dump(stamped_content, f, indent=4)
                
                st.write(f"✅ Generated: `{new_filename}`")
                
            st.success("All Logic Map files created in /output.")

    elif task == "View Logic":
        st.info("Viewer module in development.")

    elif task == "Audit (Test)":
        st.info("Audit & Validation module in development.")

# --- 6. EXECUTION ENTRY POINT ---
if __name__ == "__main__":
    main()
