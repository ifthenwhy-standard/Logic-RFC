# engines/edit_tools/ui_components.py

import streamlit as st

def render_registry_row(k, v, is_prot, selected_label):
    """
    Renders a single row in the Logic RFC table.
    Returns the (potentially) updated value and a boolean for deletion.
    """
    c1, c2, c3 = st.columns([3, 5, 1.5])
    
    with c1:
        # Key is always disabled to protect the Map schema
        st.text_input("K", value=k, disabled=True, key=f"k_{k}_{selected_label}", label_visibility="collapsed")
    
    with c2:
        # Value is disabled only if it's a Protected Protocol field
        updated_val = st.text_input("V", value=str(v), disabled=is_prot, key=f"v_{k}_{selected_label}", label_visibility="collapsed")
    
    with c3:
        to_delete = False
        if is_prot:
            st.write("🔒") # Protocol Anchor
        else:
            # Button type 'secondary' keeps it narrow and red per your CSS
            if st.button("Delete", key=f"del_{k}_{selected_label}", type="secondary"):
                to_delete = True
    
    return updated_val, to_delete