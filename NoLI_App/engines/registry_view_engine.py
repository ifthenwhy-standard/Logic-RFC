# NoLI_App/engines/registry_engine.py

import json
import re
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

def run_registry_view_workflow(PATHS, get_registry_data, load_json_registry):
    """
    Registry View Engine: Renders the high-fidelity Logic RFC table.
    """
    st.title("NoLI: Logic Registry")
    
    # 1. Fetch the metadata through the registry specialist
    metrics = get_registry_data(PATHS, load_json_registry)      
    
    if not metrics:
        st.warning("No logic maps found. Please forge a new metric manifest.")
    else:
        # 2. Build the HTML rows dynamically
        rows = "".join([
            f"<tr><td>»</td><td>{m['itw_id']}</td><td>{m['category']}</td>"
            f"<td>{m['isic']}</td><td>{m['div']}</td><td>{m['name']}</td>"
            f"<td>{m['details']}</td></tr>" 
            for m in metrics
        ])
        
        # 3. Define the styling and structure (preserving your specific design)
        registry_html = f"""
        <div class="itw-wrapper">
            <style>
                table {{ width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 11px; }}
                th {{ background: #f4f4f4; padding: 12px; border-bottom: 2px solid #333; position: sticky; top: 0; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #eee; }}
                tr:hover {{ background: #f9f9f9; }}
                .itw-wrapper {{ height: 600px; overflow-y: auto; border: 1px solid #ddd; }}
            </style>
            <table>
                <thead>
                    <tr>
                        <th>Link</th><th>ITW_ID</th><th>Persona</th>
                        <th>ISIC</th><th>Div</th><th>Metric_Name</th><th>Intent Details</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        """
        
        # 4. Render the component
        components.html(registry_html, height=650, scrolling=True)

def get_registry_data(paths, load_json_func):
    """
    Aggregates MAN and SEM files into a unified Logic Registry.
    This is the core engine for generating the NoLI view.
    """
    metrics_map = {}
    all_files = list(paths["spec"].glob("*.json"))
    
    # Load reference labels
    sections = load_json_func("ISIC_Industry_Section_Codes.json") or []
    section_map = {s.get("ISIC Section"): s.get("Industry Sector Name") for s in sections}

    for f_path in all_files:
        # Avoid processing non-spec directories
        if any(x in str(f_path) for x in ["registry", "templates", "output"]):
            continue
        
        # Only process Manifests and Semantic layers
        if not (f_path.name.startswith("MAN_") or f_path.name.startswith("SEM_")):
            continue
            
        try:
            parts = f_path.name.split('_')
            if len(parts) < 2: continue
            full_id = parts[1].replace(".json", "")
            
            # Initialize entry if not seen
            if full_id not in metrics_map:
                sec_match = re.search(r'-([A-Z])(?:\.|$)', full_id)
                div_match = re.search(r'\.([0-9]{2})(?:\.|$)', full_id)
                sec_letter = sec_match.group(1) if sec_match else "N/A"
                
                metrics_map[full_id] = {
                    "itw_id": full_id, 
                    "category": section_map.get(sec_letter, "General"), 
                    "isic": sec_letter, 
                    "div": div_match.group(1) if div_match else "--",
                    "name": "Unknown", 
                    "details": "No intent recorded"
                }
            
            with open(f_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                content = data[0] if isinstance(data, list) else data
                
                # Apply labels from MAN files
                if f_path.name.startswith("MAN_"):
                    name = content.get("metric_name") or content.get("Metric_Name")
                    if name: metrics_map[full_id]["name"] = name
                
                # Apply intent from SEM files
                if f_path.name.startswith("SEM_"):
                    details = content.get("business_why") or content.get("Business_Why")
                    if details: metrics_map[full_id]["details"] = details
        except Exception:
            continue
            
    return sorted(metrics_map.values(), key=lambda x: x['itw_id'])