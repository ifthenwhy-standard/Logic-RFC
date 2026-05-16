# engines/edit_tools/prompt_library.py
import streamlit as st
from edit_tools.prompt_intel import get_keyword_suggestions
from edit_tools.prompt_row_matrix import render_prompt_row

def render_prompt_suggestion_library(prefix, itw_id, disk_content):
    """
    Main Prompt Drawer: Captures natural language inputs and coordinates
    the master injection button framework with a high-visibility expanding canvas.
    """
    state_prompt_key = f"staged_prompt_additions_{prefix}_{itw_id}"
    if state_prompt_key not in st.session_state:
        st.session_state[state_prompt_key] = {}
        
    st.markdown("---")
    with st.expander("🤖 Suggest Fields via AI/Keyword Prompt", expanded=False):
        st.markdown("##### Natural Language Blueprinting: Discover fields by typing a concept")
        
        # --- HIGH VISIBILITY COLOR LABEL ---
        # Using markdown with an inline style to create a bold, colored callout
        st.markdown(
            "<span style='color: #FF4B4B; font-weight: bold;'>💡 Need more room? Check the box below to enlarge your typing canvas:</span>", 
            unsafe_allow_html=True
        )
        
        # The checkbox handles the action, but its label is clean and minimal
        enlarge_canvas = st.checkbox(
            "Enlarge Prompt Canvas", 
            key=f"expand_box_{prefix}_{itw_id}"
        )
        
        if enlarge_canvas:
            user_prompt = st.text_area(
                "Describe your business rules or intent in depth:",
                placeholder="Type or paste a full sentence here detailing your metrics, tracking properties, or target rules...",
                height=150,
                key=f"input_prompt_{prefix}_{itw_id}"
            )
        else:
            user_prompt = st.text_input(
                "What business parameters do you need to map?",
                placeholder="e.g., status definitions or ownership fields",
                key=f"input_prompt_{prefix}_{itw_id}"
            )
        
        suggestion_rows = get_keyword_suggestions(prefix, user_prompt)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- MASTER BUTTON ---
        staged_dict = st.session_state[state_prompt_key]
        has_hidden_selections = any(not meta.get("is_visible", False) for meta in staged_dict.values())
        master_btn_label = "📥 Insert Selected Fields" if has_hidden_selections else "📥 No Fields Selected"
        
        if st.button(master_btn_label, type="secondary", disabled=not has_hidden_selections, use_container_width=True, key=f"prompt_m_btn_{prefix}_{itw_id}"):
            shared_workspace_key = f"staged_additions_{prefix}_{itw_id}"
            for k, meta in staged_dict.items():
                if not meta.get("is_visible"):
                    staged_dict[k]["is_visible"] = True
                    st.session_state[shared_workspace_key][k] = {"value": meta["value"], "source_id": meta["source_id"], "is_visible": True}
            st.session_state[state_prompt_key] = {}
            st.success("Selected prompt items injected into your active editor below.")
            st.rerun()

        st.markdown("---")
        
        if user_prompt and not suggestion_rows:
            st.caption("No matching footprints found in the asset repository.")
        elif not user_prompt:
            st.caption("Type a phrase above to crawl your architecture library.")
        else:
            for field_key, field_val, tracking_id in suggestion_rows:
                render_prompt_row(field_key, field_val, tracking_id, prefix, itw_id, staged_dict, disk_content, state_prompt_key)