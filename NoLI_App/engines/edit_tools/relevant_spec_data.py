# engines/edit_tools/relevant_spec_data.py

import os
import sys
from pathlib import Path

# 1. DYNAMICALLY ANCHOR THE PROJECT ROOT (NoLI_App)
root_path = Path(__file__).resolve().parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# 2. SAFE INTERNAL IMPORTS
from utils.config_logic import PROTECTED_FIELDS

# Ensure the local edit_tools directory is also in path for finding spec_files_dict
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from spec_files_dict import get_spec_files_dictionary


def filter_to_prefix(prefix, sort_by="key"):
    """
    Scans all valid specifications and collects data fields matching a specific
    3-letter architecture prefix (e.g., 'SEM') across ALL matching files.
    
    Parameters:
      - prefix (str): The architectural layer to target (e.g., 'SEM', 'BRG')
      - sort_by (str): Either "key" to group rows by attribute name, or "id" 
                       to group rows by their specific ITW tracking number.
    
    Returns:
      - A sorted list of tuples: (Key, Value, Tracking_ID)
    """
    prefix_elements = []
    
    # Normalize the incoming string arguments
    target_prefix = str(prefix).strip().upper()
    sort_mode = str(sort_by).strip().lower()
    
    # Define explicit fields to strip out alongside standard global config rules
    EXCLUDED_FIELDS = {
        "current_editor", 
        "author_role", 
        "governance_status"
    }
    
    # Gather the master spec files data map from your repository scanner
    master_spec_dict = get_spec_files_dictionary(spec_path=None)
    
    for filename, file_content in master_spec_dict.items():
        # Look through ALL files that possess the designated architectural tracking prefix
        if file_content.get("Prefix") == target_prefix:
            
            # Extract the raw 12-character identification key variant from the filename string
            display_itw_id = filename[:12]
            
            # Process individual file records to unpack schemas
            for key, value in file_content.items():
                lowercased_key = key.lower()
                
                # Filter conditions: Skip structural metadata keys, global protected anchors, 
                # and explicitly targeted exclusion fields
                if (key in ["Prefix", "Filename"] or 
                    lowercased_key in PROTECTED_FIELDS or 
                    lowercased_key in EXCLUDED_FIELDS):
                    continue
                
                # Append the row metadata tuple sequence directly to our collection list
                prefix_elements.append((key, value, display_itw_id))
                
    # 3. DYNAMIC SORTING MECHANICS
    if sort_mode == "id":
        # Sort primarily by the Tracking ID (x[2]), then secondarily by Key Name (x[0])
        sorted_elements = sorted(prefix_elements, key=lambda x: (x[2], x[0]))
    else:
        # Default: Sort primarily by the Key Name (x[0]), then secondarily by Tracking ID (x[2])
        sorted_elements = sorted(prefix_elements, key=lambda x: (x[0], x[2]))
                
    return sorted_elements


# Temporary integrated unit checking framework
if __name__ == "__main__":
    print("\n--- Testing Sort by KEY Name (Default) ---")
    key_sorted = filter_to_prefix("SEM", sort_by="key")
    for row in key_sorted[:3]:
        print(f"Row Record -> Key: {row[0]:<20} | ID: {row[2]:<15} | Value: {row[1][:40]}...")

    print("\n--- Testing Sort by ITW Tracking ID ---")
    id_sorted = filter_to_prefix("SEM", sort_by="id")
    for row in id_sorted[:3]:
        print(f"Row Record -> ID: {row[2]:<15} | Key: {row[0]:<20} | Value: {row[1][:40]}...")