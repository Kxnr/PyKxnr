def change_key(old_key, new_key, dictionary):
    if old_key not in dictionary:
        raise Exception("key does not exist")

    dictionary[new_key] = dictionary.pop(old_key)
    return dictionary


def filter_keys(wanted_keys, dictionary):
    return {k: dictionary[k] for k in wanted_keys if k in dictionary}


def discard_keys(unwanted_keys, dictionary):
    return {k: dictionary[k] for k in dictionary.keys() if k not in unwanted_keys}
