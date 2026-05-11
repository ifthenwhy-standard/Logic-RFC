import streamlit as st
import streamlit.components.v1 as components
import os
import json
from pathlib import Path
from datetime import datetime
import re

# NEW IMPORT: Pulling the engine from the sub-directory
from engines.registry_view_engine import get_registry_data
from engines.bert_audit_engine import run_bert_audit_workflow
from engines.dioptras_audit_engine import run_dioptras_audit_workflow
from engines.forge_engine import run_forge_workflow
from engines.edit_engine import run_edit_workflow
from engines.registry_view_engine import run_registry_view_workflow
from utils.sidebar_manager import render_sidebar

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


# --- 4. MAIN INTERFACE ---
def main():
# Call the sidebar and return our 'task'
    task = render_sidebar(LOGO_URL, BLUEPRINT_URL)
   
    if task ==  "View Logic":
            run_registry_view_workflow(PATHS, get_registry_data, load_json_registry)    

    elif task == "Edit Logic Maps":
            run_edit_workflow(PATHS, get_all_spec_files, extract_itw_display_name)

    elif task == "Forge (Create)":
            run_forge_workflow(PATHS, load_json_registry, get_next_available_id)

    elif task == "Audit (DIOPTRAS)":
        # We pass the tools the engine needs to do its job
        run_dioptras_audit_workflow(
            PATHS, 
            get_registry_data, 
            load_json_registry
        )
    
    elif task == "Audit (BERT)":
            run_bert_audit_workflow(PATHS, get_registry_data, load_json_registry)

# --- 5. LOGIC RFC ARCHITECTURE HANDLERS ---
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