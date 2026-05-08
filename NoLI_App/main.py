import streamlit as st
import os
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

# --- Configuration & Assets ---
BLUEPRINT_ICON = "https://raw.githubusercontent.com/ifthenwhy-standard/Logic-RFC/main/images./blueprint.svg"

# SETUP
st.set_page_config(page_title="No Lie Logic Intent - IfThenWhy™")


# HEADLINE
st.title("NoLI - IfThenWhy™")
st.markdown("""
### High-Fidelity Logic Maps for Deterministic Data
Mapping human intent in structured **Logic and Data Map files**.

* **For Business Leaders:** The "Why" and the calculation behind the metric or action.
* **For DBAs & Data Analysts:** A deterministic roadmap of source-to-target mappings—without reverse-engineering code to find the truth.
* **For Auditors:** An audit trail of business logic.
* **For AI Agents:** Grounding metadata that replaces probabilistic "guesses" with authoritative, human-verified business rules.
""")

st.markdown("---")

# --- EXECUTION ---
st.markdown("")

# Call the function here so the paths are ready to use
paths = init_workspace()

if st.button("Info"):
    #st.toast("Coming Soon!")
    st.success(f"""
    ### <img src="{BLUEPRINT_ICON}" width="35" style="vertical-align: middle; margin-right: 10px;"> Coming soon!
    
    The NoLI Application has successfully processed your request:
    
    * **Create/Edit:** Logic map files updated in the repository.
    * **Convert:** SQL code successfully mapped to structured Logic RFC.
    * **Audit:** Full audit report of logic map files generated.
    * **Validation:** AI results tested using **RAGAS** and **BERT** metrics.
    * **Browse:** Repository is now refreshed with the latest IfThenWhy logic.
    """)
    
    
    # Show the "Worker Bee" the math is working
    #st.write("### Directory Mapping:")
    #for key, value in paths.items():
    #    st.code(f"{key}: {value}")