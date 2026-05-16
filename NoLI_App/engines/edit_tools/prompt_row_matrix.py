# engines/edit_tools/prompt_row_matrix.py
import streamlit as st

def render_prompt_row(field_key, field_val, tracking_id, prefix, itw_id, staged_dict, disk_content, state_prompt_key):
    """
    Renders an individual AI/Research suggestion row with a distinct,
    high-visibility background styling to denote external discovery.
    """
    # Check if this item is already sitting in our staging area or already on disk
    is_staged = field_key in staged_dict
    is_on_disk = field_key in disk_content
    
    # ─── VISUAL CONTAINER FOR HIGHLIGHTING ───
    # We use an informational/warning style container to give it a soft, distinct background glow
    with st.container(border=True):
        # A subtle micro-badge at the top of the container to scream "External Discovery"
        st.markdown(
            f"<span style='background-color: #FFEAA7; color: #D63031; padding: 2px 6px; "
            f"border-radius: 4px; font-size: 11px; font-weight: bold; font-family: monospace;'>"
            f"💡 AI RESEARCH MATCH [{tracking_id}]</span>", 
            unsafe_allow_html=True
        )
        
        # Build our crisp 4-column layout inside the highlighted box
        col_id, col_k, col_v, col_btn = st.columns([1.5, 3, 5, 2])
        
        with col_id:
            st.code(tracking_id, language=None)
            
        with col_k:
            st.markdown(f"**`{field_key}`**")
            
        with col_v:
            st.text(field_val)
            
        with col_btn:
            if is_on_disk:
                st.button("In File", disabled=True, key=f"p_disk_{field_key}_{prefix}_{itw_id}", use_container_width=True)
            elif is_staged:
                st.button("Staged", disabled=True, key=f"p_stg_{field_key}_{prefix}_{itw_id}", use_container_width=True)
            else:
                # Active button to capture the new key-value pairing
                if st.button("Add", type="primary", key=f"p_add_{field_key}_{prefix}_{itw_id}", use_container_width=True):
                    staged_dict[field_key] = {
                        "value": field_val,
                        "source_id": tracking_id,
                        "is_visible": False  # Stays hidden until master "Insert" button is clicked
                    }
                    st.rerun()