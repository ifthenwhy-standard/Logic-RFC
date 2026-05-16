# engines/edit_tools/active_workspace.py
import streamlit as st
from edit_tools.file_utilities import get_logic_metadata_dict
from edit_tools.ui_components import render_registry_row
from utils.config_logic import PROTECTED_FIELDS

def render_active_workspace(PATHS, itw_id, sorted_keys, disk_content, selected_label, updated_content):
    """
    Renders baseline metadata context and loops through elements currently saved on disk.
    """
    logic_context = get_logic_metadata_dict(PATHS, itw_id, prefix="SEM")

    if logic_context.get("business_owner"):
        st.caption(f"Strategy Lead: {logic_context.get('business_owner')}")

    st.markdown("---")
    
    for k in sorted_keys:
        is_prot = k.lower() in PROTECTED_FIELDS
        val, delete_clicked = render_registry_row(k, disk_content[k], is_prot, selected_label)
        
        if not delete_clicked:
            updated_content[k] = val