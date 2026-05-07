import streamlit as st
import json
import os
import re
from datetime import datetime
from pathlib import Path

# --- WORKSPACE INITIALIZATION ---
def init_workspace():
    # APP_DIR is /NoLI_App
    APP_DIR = Path(__file__).resolve().parent
    paths = {
        "templates": APP_DIR.parent / "templates",
        "registry": APP_DIR.parent / "spec" / "registry",
        "output": APP_DIR.parent / "output",
        "spec": APP_DIR.parent / "spec"
    }
    
    # Ensure output exists (The "Worker Bee" desk is clean)
    os.makedirs(paths["output"], exist_ok=True)
    return paths

# Call init once and store in a variable
PATHS = init_workspace()

# --- HELPER FUNCTIONS ---
@st.cache_data # This tells Streamlit to remember the data and not "re-run" the file read
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
            # Standard Metadata Stamping
            if k.lower().replace("-", "_") == "itw_id": obj[k] = itw_id
            elif k.lower() == "metric_id": obj[k] = metric_id
            elif k.lower() == "framework": obj[k] = "IfThenWhy"
            elif k.lower() == "last_updated": obj[k] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # File-Specific Content Stamping (SEM, BRG, LDD, etc.)
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

# --- MAIN APP INTERFACE ---
def main():
    st.set_page_config(page_title="NoLI App", page_icon="🚨")

    st.sidebar.title("NoLI™ Workspace")
    st.sidebar.markdown("*Fluent in Human. No-Lie Logic Intent.*")
    task = st.sidebar.radio("Select Task", ["View Logic", "Forge (Edit)", "Audit (Test)"])

    st.title(f"NoLI: {task}")

    if task == "Forge (Edit)":
        st.header("Logic RFC™: Precision Builder")
        
        # Load Registry Files (Cached for speed)
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

        # ITW_ID Generation Logic
        pcf_val = str(pcf['PCF Code']).split('.')[-1].zfill(2)
        div_clean = re.sub(r'\D', '', str(division['ISIC Division']))[-3:].zfill(3)
        full_itw_id = f"itw_{unique_id}.{pcf_val}.{sec_letter}.{div_clean}.{corp_id}.{ver_num}"
        
        st.info(f"**Target ITW_ID:** `{full_itw_id}`")

        if st.button("Forge Logic DNA Files"):
            templates = list(PATHS["templates"].glob("*.json"))
            for t_path in templates:
                with open(t_path, 'r') as f:
                    template_data = json.load(f)
                
                prefix = t_path.name.split('_')[0]
                new_filename = f"{prefix}_ITW-{unique_id}.{pcf_val}-{sec_letter}.{div_clean}.{corp_id}.{ver_num}.json"
                
                # Stamp the DNA
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

# Ensure the app runs correctly
if __name__ == "__main__":
    main()