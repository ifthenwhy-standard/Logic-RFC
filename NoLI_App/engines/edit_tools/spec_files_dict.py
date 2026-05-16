# engines/edit_tools/spec_files_dict.py

import os
import json

def get_spec_files_dictionary(spec_path=None):
    """
    Loops through all JSON files in the /spec directory and returns a dictionary 
    mapping each filename to its parsed metadata properties (Prefix, Filename, itw_id)
    alongside ALL key-value pairs stored inside that JSON file.
    
    Explicitly filters out non-spec files like readme.md.
    """
    spec_dict = {}
    
    # If no path is provided, dynamically find /Logic-RFC/spec relative to this script file
    if spec_path is None:
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        spec_path = os.path.abspath(os.path.join(current_script_dir, "..", "..", "..", "spec"))

    # Ensure the directory exists before scanning
    if not os.path.exists(spec_path):
        print(f"⚠️ Debug: Evaluated spec path does not exist: {spec_path}")
        return spec_dict

    for filename in os.listdir(spec_path):
        # Clean downcase handling for strict filter matching
        lower_filename = filename.lower()
        
        # Airtight check: Must be a .json file AND cannot be a readme document
        if lower_filename.endswith(".json") and not lower_filename.startswith("readme"):
            
            # 1. Extract structural metadata from filename
            prefix = filename[:3].upper()
            itw_id = filename[4:12].upper() # Fallback short ID parser
            
            # 2. Establish the baseline metadata properties
            file_entry = {
                "Prefix": prefix,
                "Filename": filename,
                "itw_id": itw_id
            }
            
            # 3. Read and inject all key-value pairs from the physical JSON file
            file_absolute_path = os.path.join(spec_path, filename)
            try:
                with open(file_absolute_path, "r", encoding="utf-8") as f:
                    file_data = json.load(f)
                    
                    # Unpack array wrapping if the file matches that layout format
                    content = file_data[0] if isinstance(file_data, list) else file_data
                    
                    # Merge all file content keys directly into our file_entry dictionary
                    file_entry.update(content)
                    
                    # Governance Guardrail: Ensure itw_id reflects the precise internal file truth 
                    # if it exists, overriding the rough 8-character filename slice.
                    if "itw_id" in content:
                        file_entry["itw_id"] = content["itw_id"]
                    elif "ITW_ID" in content:
                        file_entry["itw_id"] = content["ITW_ID"]
                        
            except Exception as e:
                print(f"⚠️ Error reading JSON contents for file {filename}: {e}")
                continue # Skip corrupt files to preserve dictionary health
            
            # 4. Bind the enriched properties to the root filename key
            spec_dict[filename] = file_entry
            
    return spec_dict

# Temporary built-in test block
if __name__ == "__main__":
    results = get_spec_files_dictionary(spec_path=None)
    
    print("\n--- Direct Script Test Output ---")
    if not results:
        print("Dictionary is empty. Check if your JSON files are inside /Logic-RFC/spec")
    else:
        print(json.dumps(results, indent=4))


