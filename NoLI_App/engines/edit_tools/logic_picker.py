# engines/edit_tools/logic_picker.py

import os
import json

def get_itw_picker_data(spec_path='./Logic-RFC/spec'):
    """
    Scans /spec for JSON files, groups by 3-letter prefix, 
    and returns a dict for Streamlit selectboxes.
    """
    picker_data = {}
    if not os.path.exists(spec_path):
        return {}

    for filename in os.listdir(spec_path):
        if filename.endswith(".json"):
            prefix = filename[:3].upper()
            file_path = os.path.join(spec_path, filename)
            
            if prefix not in picker_data:
                picker_data[prefix] = []

            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    # Custom parsing for your 'no-brackets' flat JSON format
                    json_objects = f"[{content.replace('}{', '},{')}]"
                    data = json.loads(json_objects)
                    
                    for entry in data:
                        itw_id = entry.get('ITW_ID') or entry.get('ITW-ID')
                        # Logic RFC priority: SEM text first, then Description
                        desc = entry.get('SEM') or entry.get('Description') or "No Description"
                        
                        picker_data[prefix].append({
                            "id": itw_id,
                            "display": f"{itw_id} | {desc[:55]}...",
                            "filename": filename
                        })
            except Exception:
                continue # Skip files that don't match the expected Logic DNA
    return picker_data