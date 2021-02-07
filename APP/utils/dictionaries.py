def copy_dict(source_dict, diffs):
    """Returns a copy of source_dict, updated with the new key-value
       pairs in diffs."""
    result = dict(source_dict)  # Shallow copy, see addendum below
    result.update(diffs)
    return result
