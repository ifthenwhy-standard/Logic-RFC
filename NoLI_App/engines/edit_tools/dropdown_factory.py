# engines/edit_tools/dropdown_factory.py


from utils.config_logic import TYPE_LABELS

from edit_tools.file_utilities import get_protocol_description 


def build_edit_dropdown_options(PATHS, spec_files, extract_itw_display_name):
    """
    Builds the descriptive dictionary and label list for the selectbox.
    """
    file_map = {}
    display_options = []
    
    for f in spec_files:
        itw_id = extract_itw_display_name(f.name)
        prefix = f.name.split('_')[0] if '_' in f.name else ""
        type_label = TYPE_LABELS.get(prefix, prefix)
        
        # Peer into SEM for the descriptive name (logic_map_name)
        desc = get_protocol_description(PATHS, itw_id)
        
        # Format: ITW_001 Revenue Map (Manifest)
        display_label = f"{itw_id} {desc} ({type_label})".strip()
        
        file_map[display_label] = f
        display_options.append(display_label)
        
    return file_map, sorted(display_options)