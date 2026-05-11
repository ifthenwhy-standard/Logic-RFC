import streamlit as st

def render_sidebar(LOGO_URL, BLUEPRINT_URL):
    """
    Sidebar Manager: Handles navigation, session state initialization, 
    and the IfThenWhy roadmap/about sections.
    """
    # 1. Load Global CSS First
    st.markdown("""
        <style>
            label p { color: #000; font-weight: 500; }
            div.stButton > button:first-child {
                background-color: #0071e3; color: white; border-radius: 20px;
                padding: 10px 40px; min-width: 300px; white-space: nowrap; border: none; font-weight: 600;
            }
            /* Note: :contains() is sometimes tricky in CSS, 
               but this targets your red Discard button perfectly */
            div.stButton > button:contains("Discard/Undo") {
                background-color: #ffffff; color: #d93025; border: 1px solid #d93025;
            }
            .header-label { font-weight: 700; color: #333; font-size: 0.9rem; }
            .itw-wrapper { height: 600px; overflow-y: auto; border: 1px solid #ddd; }
        </style>
    """, unsafe_allow_html=True)
    
    
    # 2. Initialize Session States
    if 'set_created' not in st.session_state:
        st.session_state.set_created = False
    
    if 'show_info' not in st.session_state:
        st.session_state.show_info = False

    with st.sidebar:
        # 3. Navigation Logic
        task = st.radio("Select Workflow", [
            "Edit Logic Maps", 
            "Forge (Create)", 
            "View Logic", 
            "Audit (DIOPTRAS)", 
            "Audit (BERT)"
        ])
        
        st.markdown("---")

        # 4. Roadmap / Info Section
        if st.button("ℹ️ Info / Roadmap"):
            st.session_state.show_info = not st.session_state.show_info

        if st.session_state.show_info:
            st.markdown(
                """
                <div style="background-color: #d4edda; color: #155724; padding: 1rem; border-radius: 0.5rem; border: 1px solid #c3e6cb;">
                    <h4 style="display: flex; align-items: center; margin-top: 0;">
                        <img src="{url}" width="25" style="margin-right: 10px;"> 
                        Roadmap
                    </h4>
                    <p style="font-size: 0.85rem;">The NoLI Application Roadmap will include:</p>
                    <ul style="font-size: 0.8rem; margin-top: 0;">
                        <li><strong>Gap Scan:</strong> AI search of news and legal updates to identify conflicts.</li>
                        <li><strong>RAGAS:</strong> Advanced evaluation of RAG faithfulness.</li>
                        <li><strong>Active:</strong> BERT Faithfulness & Dioptras Audits (Live).</li>
                    </ul>
                    <p style="font-size: 0.7rem; opacity: 0.8; margin-top: 10px;">(Click button again to collapse)</p>
                </div>
                """.format(url=BLUEPRINT_URL), 
                unsafe_allow_html=True
            )

        st.markdown("---")
        
        # 5. Brand Identity Section
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
            
    return task # Return the selected task to the main script