# engines/edit_tools/view_library.py
import streamlit as st
from edit_tools.relevant_spec_data import filter_to_prefix

def render_suggestion_library(prefix, itw_id, state_additions_key, disk_content):
    """
    Renders the reference repository pool expander with its sorting choices,
    dynamic master 'Insert' button, and tracking row states.
    """
    st.markdown("---")
    with st.expander("📂 View Library of Files for suggestions", expanded=False):
        st.markdown(
            f"##### Reference Repository Pool: Exploring other `{prefix}` architecture footprints"
        )
        
        sort_choice = st.radio(
            "Group library items by:",
            options=["Field / Key Name", "ITW Tracking ID"],
            horizontal=True,
            key=f"lib_sort_{prefix}_{itw_id}"
        )
        
        sort_mode = "key" if "Field" in sort_choice else "id"
        suggestion_rows = filter_to_prefix(prefix, sort_by=sort_mode)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- DYNAMIC MASTER BUTTON STATE ---
        staged_dict = st.session_state[state_additions_key]
        has_hidden_selections = any(not meta.get("is_visible", False) for meta in staged_dict.values())
        
        master_btn_label = "📥 Insert Selected Fields" if has_hidden_selections else "📥 No Fields Selected"
        
        if st.button(
            master_btn_label, 
            type="secondary", 
            disabled=not has_hidden_selections,
            use_container_width=True,
            key=f"pull_btn_{prefix}_{itw_id}"
        ):
            for k in staged_dict:
                staged_dict[k]["is_visible"] = True
            st.success("Selected fields injected into the editor canvas below.")
            st.rerun()

        st.markdown("---")
        
        if not suggestion_rows:
            st.caption(f"No companion `{prefix}` specification documents found in the asset pool.")
            return

        # 4-Column Layout Matrix
        for field_key, field_val, tracking_id in suggestion_rows:
            row_uid = f"lib_{field_key}_{tracking_id}_{prefix}_{itw_id}"
            c1, c2, c3, c4 = st.columns([1.5, 2, 4.5, 1])
            
            with c1:
                st.text_area("ID", value=tracking_id, disabled=True, height=68, key=f"id_{row_uid}", label_visibility="collapsed")
            with c2:
                st.text_area("K", value=field_key, disabled=True, height=68, key=f"k_{row_uid}", label_visibility="collapsed")
            with c3:
                st.text_area("V", value=str(field_val), disabled=True, height=68, key=f"v_{row_uid}", label_visibility="collapsed")
            with c4:
                st.markdown("<div style='padding-top:15px;'></div>", unsafe_allow_html=True)
                
                is_already_staged = field_key in staged_dict
                btn_label = "Staged" if is_already_staged else "Add"
                
                if st.button(btn_label, key=f"btn_{row_uid}", type="secondary", disabled=is_already_staged):
                    if field_key not in disk_content:
                        st.session_state[state_additions_key][field_key] = {
                            "value": str(field_val),
                            "source_id": tracking_id,
                            "is_visible": False
                        }
                        st.toast(f"Staged suggestion: {field_key}")
                        st.rerun()