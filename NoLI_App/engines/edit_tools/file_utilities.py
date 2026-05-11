# engines/edit_tools/file_utilities.py

import json

def get_protocol_description(PATHS, itw_id):
    """
    Peeks into the SEM file to extract the 'logic_map_name'.
    The SEM file remains the source of truth for human-readable labels.
    """
    target_maps = list(PATHS["spec"].glob(f"**/SEM_{itw_id}*.json"))
    
    if target_maps:
        try:
            with open(target_maps[0], 'r', encoding='utf-8') as f:
                data = json.load(f)
                content = data[0] if isinstance(data, list) else data
                return content.get("logic_map_name", "")
        except Exception:
            return ""
    return ""

def get_logic_metadata_dict(PATHS, itw_id, prefix="SEM"):
    """
    Returns a dictionary of all keys and values from any requested logic map file.
    Default prefix is 'SEM', but works for 'DIC', 'BRG', 'LDD', or 'LUT'.
    """
    map_files = list(PATHS["spec"].glob(f"**/{prefix}_{itw_id}*.json"))
    
    if map_files:
        try:
            with open(map_files[0], 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data[0] if isinstance(data, list) else data
        except Exception:
            return {}
    return {}