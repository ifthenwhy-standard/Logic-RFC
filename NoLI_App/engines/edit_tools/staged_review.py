# engines/edit_tools/staged_review.py
import streamlit as st
from edit_tools.editor_mechanics import save_logic_changes

def render_staged_review(state_additions_key, selected_label, updated_content, target_path):
    """
    Renders fields unlocked by the user using 'Insert Selected Fields' and handles disk synchronization.
    """
    staged_items = st.session_state[state_additions_key]
    visible_staged_items = {k: meta for k, meta in staged_items.items() if meta.get("is_visible")}
    
    if visible_staged_items:
        st.markdown("##### Newly Added Suggestion Elements")
        
        for k, meta in list(visible_staged_items.items()):
            v = meta["value"]
            src_id = meta["source_id"]
            
            c1, c2, c3, c4 = st.columns([1.5, 2, 4.5, 1])
            
            with c1:
                st.text_area("ID", value=src_id, disabled=True, height=68, key=f"staged_id_{k}_{selected_label}", label_visibility="collapsed")
            with c2:
                st.text_area("K", value=k, disabled=True, height=68, key=f"staged_k_{k}_{selected_label}", label_visibility="collapsed")
            with c3:
                updated_staged_val = st.text_area("V", value=v, disabled=False, height=68, key=f"staged_v_{k}_{selected_label}", label_visibility="collapsed")
                st.session_state[state_additions_key][k]["value"] = updated_staged_val
                updated_content[k] = updated_staged_val
            with c4:
                st.markdown("<div style='padding-top:5px; font-weight:bold; font-size:13px; color:#0073e6;'>✨ new</div>", unsafe_allow_html=True)
                if st.button("Remove", key=f"rem_staged_{k}_{selected_label}", type="secondary"):
                    del st.session_state[state_additions_key][k]
                    st.rerun()

    # --- THE STRATEGIC INTENT (The Why) ---
    st.markdown("---")
    if st.button("Save Changes", type="primary"):
        if save_logic_changes(target_path, updated_content):
            st.session_state[state_additions_key] = {}
            st.success("Logic Synchronized. Suggestions committed directly to schema.")
            st.rerun()