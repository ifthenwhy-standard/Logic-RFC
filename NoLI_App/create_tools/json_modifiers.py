# json_modifiers
def update_nested_keys(data, updates):
    """Recursively walks through a dictionary/list to update matching keys in-place."""
    if isinstance(data, dict):
        for k, v in data.items():
            if k in updates:
                data[k] = updates[k]
            else:
                update_nested_keys(v, updates)
    elif isinstance(data, list):
        for item in data:
            update_nested_keys(item, updates)