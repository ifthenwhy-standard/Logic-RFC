# template_injector.py

# template_injector
import os
import json

def build_fallback_schema():
    """Generates a default multi-layered structural layout if a template file is missing."""
    return [{
        "Protocol_Governance": {
            "Framework_Status": "Thought Leadership Protocol"
        },
        "Metadata": {},
        "Metric_Definition": {}
    }]

def inject_metadata_bounds(target_dict, full_itw_id, logic_map_name, pref, current_timestamp):
    """
    Safely traverses template components to inject core runtime identity boundaries
    into both top-level and deep sub-object shapes.
    """
    if not isinstance(target_dict, dict):
        return
    
    # Root Structure Synchronization
    target_dict["itw_id"] = full_itw_id
    target_dict["metric_name"] = logic_map_name
    target_dict["tier_prefix"] = pref
    target_dict["version"] = "001"
    target_dict["last_updated"] = current_timestamp
    
    # Deep Metadata Layer Alignment
    if "Metadata" in target_dict and isinstance(target_dict["Metadata"], dict):
        target_dict["Metadata"]["itw_id"] = full_itw_id
        target_dict["Metadata"]["logic_map_name"] = logic_map_name
        target_dict["Metadata"]["last_updated"] = current_timestamp
        
    # Deep Operational Metric Definitions Mapping
    if "Metric_Definition" in target_dict and isinstance(target_dict["Metric_Definition"], dict):
        target_dict["Metric_Definition"]["logic_map_name"] = logic_map_name
        target_dict["Metric_Definition"]["metric_name"] = logic_map_name

def process_and_forge_tier(PATHS, pref, full_itw_id, logic_map_name, current_timestamp):
    """
    Reads the master template file from disk, unrolls list or dictionary payload layers, 
    injects core unique parameters, and saves the individual compiled layer.
    """
    template_dir = PATHS.get("templates", PATHS["spec"].parent / "templates")
    template_path = template_dir / f"{pref}.json"
    
    content_payload = None
    
    # Load Master Template Framework
    if os.path.exists(template_path):
        try:
            with open(template_path, "r", encoding="utf-8") as tf:
                content_payload = json.load(tf)
        except Exception:
            pass  # Fall back to structured baseline on error
            
    if content_payload is None:
        content_payload = build_fallback_schema()
        
    # Process structure based on type (JSON Array List or standard Object)
    if isinstance(content_payload, list):
        for item in content_payload:
            if isinstance(item, dict):
                inject_metadata_bounds(item, full_itw_id, logic_map_name, pref, current_timestamp)
    else:
        inject_metadata_bounds(content_payload, full_itw_id, logic_map_name, pref, current_timestamp)
        
    # Deploy populated logic specification down to target folder
    file_path = PATHS["spec"] / f"{pref}_{full_itw_id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content_payload, f, indent=4)
        
    return str(file_path)