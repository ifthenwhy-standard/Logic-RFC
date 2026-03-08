import json
import os
import re
from datetime import datetime
from pathlib import Path

# --- LOGIC RFC PATHING ---
APP_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = APP_DIR.parent / "templates"
REGISTRY_PATH = APP_DIR.parent / "spec" / "registry"
# Corrected to \output as requested
OUTPUT_PATH = APP_DIR.parent / "output" 

os.makedirs(OUTPUT_PATH, exist_ok=True)

def load_registry(filename):
    path = REGISTRY_PATH / filename
    if not path.exists(): return None
    with open(path, 'r') as f: return json.load(f)

def get_choice(options, label_key, prompt):
    print(f"\n==============================\n BROWSER: {prompt}\n==============================")
    search = input(f"Search keyword (or Enter to browse): ").strip().lower()
    filtered = [o for o in options if search in str(o.get(label_key, "")).lower()]
    if not filtered: filtered = options
    
    page_size, current_start = 10, 0
    while True:
        current_end = current_start + page_size
        display_list = filtered[current_start:current_end]
        print(f"\n--- {prompt}: {current_start + 1} to {min(current_end, len(filtered))} of {len(filtered)} ---")
        for i, opt in enumerate(display_list):
            print(f"{i + current_start + 1}. {opt[label_key]}")
        
        val = input("\nSelect: [Number] | Next: [Enter] | Prev: (p) | Search: (s)\nChoice: ").strip().lower()
        if val == "" or val == 'n':
            if current_end < len(filtered): current_start += page_size
            else: print("\n>> NOTICE: End of list.")
        elif val == 'p' and current_start > 0: current_start -= page_size
        elif val == 's': return get_choice(options, label_key, prompt)
        else:
            try:
                selection = int(val)
                if 1 <= selection <= len(filtered): return filtered[selection - 1]
            except ValueError: pass

def main():
    print("==========================================\n    Logic RFC™: Precision Builder v1.5.7   \n==========================================")
    
    # Restoring the interactive questions
    unique_id = input("\nEnter 4-Digit Metric ID: ").strip()
    metric_name = input("Enter Metric Name: ").strip()

    sections = load_registry("ISIC_Industry_Section_Codes.json")
    divisions = load_registry("ISIC_Industry_Division_Codes.json")
    pcf_cats = load_registry("PCF_Categories.json")

    section = get_choice(sections, "Industry Sector Name", "Industry Section")
    sec_letter = section.get("ISIC Section")
    filtered_divs = [d for d in divisions if d.get("ISIC Section") == sec_letter]
    division = get_choice(filtered_divs if filtered_divs else divisions, "Industry Sector / Activity Name", "Industry Division")
    pcf = get_choice(pcf_cats, "PCF Category", "PCF Category")
    
    corp_id = input("\nStatus/Company ID (Default [EXP]): ").strip().upper() or "EXP"
    ver_num = input("Version (Default [001]): ").strip() or "001"

    pcf_val = str(pcf['PCF Code']).split('.')[-1].zfill(2)
    div_clean = re.sub(r'\D', '', str(division['ISIC Division']))[-3:].zfill(3)
    full_itw_id = f"itw_{unique_id}.{pcf_val}.{sec_letter}.{div_clean}.{corp_id}.{ver_num}"

    # Template-to-Layer Matching
    template_files = list(TEMPLATE_PATH.glob("*.json"))
    for t_path in template_files:
        with open(t_path, 'r') as f:
            template_data = json.load(f)

        prefix = t_path.name.split('_')[0]
        new_filename = f"{prefix}_ITW-{unique_id}.{pcf_val}-{sec_letter}.{div_clean}.{corp_id}.{ver_num}.json"

        def inject_dna(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    # Catching various itw key formats in templates
                    if k.lower().replace("-", "_") == "itw_id": obj[k] = full_itw_id
                    elif k.lower() == "metric_id": obj[k] = f"itw_{unique_id}"
                    elif k.lower() == "framework": obj[k] = "IfThenWhy"
                    elif k.lower() == "last_updated": obj[k] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    if prefix == "MAN" and k == "metric_name": obj[k] = metric_name
                    if prefix == "BRG":
                        if k in ["Industry", "Industry_Context"]: obj[k] = section["Industry Sector Name"]
                        if k in ["Division", "Division_Context"]: obj[k] = division["Industry Sector / Activity Name"]
                    
                    if isinstance(v, (dict, list)): inject_dna(v)
            elif isinstance(obj, list):
                for item in obj: inject_dna(item)
            return obj

        stamped_content = inject_dna(template_data)
        with open(OUTPUT_PATH / new_filename, 'w') as f:
            json.dump(stamped_content, f, indent=4)
        print(f"  {prefix} saved to \output using template {t_path.name}")

if __name__ == "__main__":
    main()