# engines/edit_tools/editor_mechancis.py

import json
import streamlit as st
from datetime import datetime

def load_logic_content(file_path):
    """Opens a logic map and returns the content and sorted keys."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Handle both list and dict formats to ensure protocol flexibility
    content = data[0] if isinstance(data, list) else data
    sorted_keys = sorted(content.keys(), key=lambda x: x.lower())
    return content, sorted_keys

def save_logic_changes(file_path, updated_content):
    """Updates the audit trail and writes the new logic to disk."""
    updated_content["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(updated_content, f, indent=4)
    return True