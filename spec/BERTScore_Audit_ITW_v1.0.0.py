# ---------------------------------------------------------------------------------
# PROTOCOL GOVERNANCE: IfThenWhy / Logic RFC™[cite: 1, 4]
# STATUS: Thought Leadership Protocol (Not a service-for-hire)
# NOTICE: This script is provided 'AS IS' for logic-mapping purposes only.
# LIABILITY: The framework owner assumes no liability for AI results, pricing 
# errors, or unauthorized commitments. All final actions require validation 
# by a Human-in-the-Loop.[cite: 1, 2]
# This script is provided 'AS IS'. The owner assumes no liability for 
# AI results or revenue loss. Final approval requires Human-in-the-Loop.
# VERSION: 1.0.0 (Stable - Openpyxl Edition)
# ---------------------------------------------------------------------------------
# EXECUTION INSTRUCTION: Run this script from within the same directory as your 
# Logic RFC™ mapping files (e.g., the /spec folder on GitHub).
# This ensures the script can locate all 'SEM_ITW-' files for the audit. 
# ---------------------------------------------------------------------------------
#Install the BERTScore library via terminal before running: pip install bert-scoreimport os
# or pip3 install --user bert-score pandas
# or  pip install openpyxl bert-score
# ---------------------------------------------------------------------------------
# LIABILITY: This script is provided 'AS IS'. The owner assumes no liability for 
# AI results or revenue loss. Final approval requires Human-in-the-Loop.
# ---------------------------------------------------------------------------------

import os
import json
import openpyxl
from openpyxl import Workbook
from bert_score import score

def run_transparent_audit(mapping_folder, output_file="results.xlsx"):
    output_wb = Workbook()
    output_sheet = output_wb.active
    output_sheet.title = "Logic Audit"
    output_sheet.append(["ITW_ID", "Business_Why", "Strategic_Intent", "BERTScore_F1", "Audit_Note"])

    print(f"--- Starting Logic RFC™ Total Audit: {mapping_folder} ---")

    rows_written = 0
    for filename in sorted(os.listdir(mapping_folder)):
        # Broaden filter to catch ALL ITW SEM files
        if filename.startswith("SEM_ITW") and filename.endswith(".json"):
            sem_path = os.path.join(mapping_folder, filename)
            
            with open(sem_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    # High-fidelity check: Handle both list and dict formats
                    sem_data = data[0] if isinstance(data, list) else data
                    
                    # Pull values with Case-Insensitivity to be safe
                    itw_id = sem_data.get("ITW_ID", sem_data.get("itw_id", filename))
                    biz_why = sem_data.get("Business_Why", sem_data.get("business_why", ""))
                    strat_intent = sem_data.get("Strategic_Intent", sem_data.get("strategic_intent", ""))
                    
                    if biz_why and strat_intent:
                        # BERT calculation
                        P, R, F1 = score([biz_why], [strat_intent], lang="en", verbose=False)
                        f1_val = round(F1.item(), 4)
                        
                        output_sheet.append([itw_id, biz_why, strat_intent, f1_val, "Successful Audit"])
                        rows_written += 1
                        print(f"Audit Complete: {itw_id} | Score: {f1_val}")
                    else:
                        # This tells you EXACTLY why it's skipping
                        print(f"[SKIP]: {filename} - Found ITW_ID but missing Why or Intent keys.")
                        
                except Exception as e:
                    print(f"[ERROR]: Could not process {filename}: {e}")

    output_wb.save(output_file)
    print(f"\n--- AUDIT SUMMARY ---\nRows Written: {rows_written}")
    output_wb.save(output_file)
    print("\n--- AUDIT SUMMARY ---")
    print(f"Rows Written: {rows_written}")
    print("Logic: BERT compared the Business_Why to the Strategic_Intent")

if __name__ == "__main__":
    run_transparent_audit('.')