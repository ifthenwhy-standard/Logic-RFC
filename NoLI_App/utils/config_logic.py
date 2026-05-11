# utils/config_logic.py

# 1. PROTOCOL GOVERNANCE
# These fields are the 'anchors' of the Logic RFC. 
# They are read-only in the editor to prevent breaking the framework.
PROTECTED_FIELDS = [
    "itw_id", 
    "version", 
    "file_type", 
    "original_author", 
    "last_updated",
    "logic_map_name"
]

# Mapping for the human-readable labels in the dropdown
TYPE_LABELS = {
    "MAN": ("Manifest", "The Master Label identifying ownership and versioning."),
    "SEM": ("Semantics", "The 'Business Why' that anchors metrics to stakeholder personas."),
    "BRG": ("Bridge", "The kinetic link between a real-world event (If) and a data action (Then)."),
    "LDD": ("Logic Data Design", "The authoritative engine for mathematical proof and validation logic."),
    "DIC": ("Data Dictionary", "The physical map for source-to-target data relationships."),
    "LUT": ("Lookup Table", "The universal translator for categorical labels and hierarchies.")
}