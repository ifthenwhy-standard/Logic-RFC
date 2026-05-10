import os
import json
import re
from pathlib import Path

# --- 1. WORKSPACE INITIALIZATION ---
def init_workspace():
    """
    Anchors the framework to the true root.
    Path of this file: /Logic_RFC/NoLI_App/engines/logic_engine.py
    We go up 3 levels to reach /Logic_RFC/
    """
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    
    paths = {
        "templates": ROOT_DIR / "templates",
        "registry": ROOT_DIR / "spec" / "registry",
        "output": ROOT_DIR / "output",
        "spec": ROOT_DIR / "spec"
    }
    
    # Ensure directories exist
    for p in paths.values():
        os.makedirs(p, exist_ok=True)
    return paths

# Global PATHS variable for use across the module and imports
PATHS = init_workspace()

# --- 2. REGISTRY & FILE AGGREGATION ---

def load_json_registry(filename):
    """Loads reference metadata (ISIC, PCF, etc.) from the registry folder."""
    path = PATHS["registry"] / filename
    if not path.exists(): 
        return None
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def get_registry_data(paths):
    """
    Aggregates MAN and SEM files to build the 'View Logic' master table.
    Prioritizes ITW_ID consistency.
    """
    metrics_map = {}
    all_files = list(paths["spec"].glob("*.json"))
    
    # Load industry names for the display table
    sections = load_json_registry("ISIC_Industry_Section_Codes.json") or []
    section_map = {s.get("ISIC Section"): s.get("Industry Sector Name") for s in sections}

    for f_path in all_files:
        # Skip system folders
        if any(x in str(f_path) for x in ["registry", "templates", "output"]):
            continue
        
        # Only process Metric Manifests and Semantic Layers for the Registry View
        if not (f_path.name.startswith("MAN_") or f_path.name.startswith("SEM_")):
            continue
            
        try:
            parts = f_path.name.split('_')
            if len(parts) < 2: continue
            full_id = parts[1].replace(".json", "")
            
            if full_id not in metrics_map:
                # Parse ISIC and Division from the ITW_ID string
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
                
                if f_path.name.startswith("MAN_"):
                    name = content.get("metric_name") or content.get("Metric_Name")
                    if name: metrics_map[full_id]["name"] = name
                
                if f_path.name.startswith("SEM_"):
                    details = content.get("business_why") or content.get("Business_Why")
                    if details: metrics_map[full_id]["details"] = details
        except Exception:
            continue
            
    return sorted(metrics_map.values(), key=lambda x: x['itw_id'])

# --- 3. FILE SYSTEM HELPERS ---

def get_all_spec_files():
    """Returns a list of all JSON files in the /spec directory."""
    return list(PATHS["spec"].glob("*.json"))

def extract_itw_display_name(filename):
    """Extracts the ITW-XXXX.XXX format from a filename for dropdowns."""
    match = re.search(r'(ITW-\d{4}[^ ]*)', filename)
    return match.group(1).replace(".json", "") if match else filename

def get_next_available_id(paths):
    """Calculates the next numerical ITW ID based on existing files."""
    used_ids = []
    all_spec_files = list(paths["spec"].glob("**/*.json"))
    for f in all_spec_files:
        match = re.search(r'ITW-(\d{4})', f.name)
        if match:
            used_ids.append(int(match.group(1)))
    return max(used_ids) + 1 if used_ids else 1001