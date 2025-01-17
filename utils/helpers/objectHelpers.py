
# def hasattrdeep(object, attributes: list[str]) -> bool:
#     if len(attributes) == 0:
#         return True
#     if attributes[0] in object:
#         return hasattrdeep(object[attributes[0]], attributes[1:])
#     return False

def hasattrdeep(obj, attributes: list[str]) -> bool:
    if not isinstance(obj, dict) or len(attributes) == 0:
        return False
    if attributes[0] in obj:
        if len(attributes) == 1:
            return True
        return hasattrdeep(obj[attributes[0]], attributes[1:])
    return False

# def traverseDictAndUpdateField(fieldPath, newValue, dict):
#     if len(fieldPath) == 1:
#         dict[fieldPath[0]] = newValue
#         return dict
#     field = fieldPath.pop(0)
#     if field not in dict:
#         dict[field] = {}
#     if not type(dict[field]) == dict:
#         raise TypeError(f"Field '{field}' cannot be updated as it is not a dict")
#     dict[field] = traverseDictAndUpdateField(fieldPath, newValue, dict[field])
#     return dict

def traverseDictAndUpdateField(field_path, value, target_dict, delete=False):
    """
    Traverse a dictionary to update or delete a nested field.

    Args:
        field_path (list): List of keys representing the path to the field.
        value: The new value to set (ignored if delete=True).
        target_dict (dict): The dictionary to modify.
        delete (bool): If True, delete the field instead of updating its value.
    """
    current = target_dict
    for key in field_path[:-1]:
        current = current.setdefault(key, {})

    if delete:
        current.pop(field_path[-1], None)
    else:
        current[field_path[-1]] = value
