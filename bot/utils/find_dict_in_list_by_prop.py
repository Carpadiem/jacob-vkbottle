def find_dict_in_list_by_prop(search_in: list, where: dict):

    w_key = list(where.keys())[0]
    w_value = list(where.values())[0]

    try:
        obj = list(filter(lambda item: item[w_key] == w_value, search_in))[0]
    except IndexError:
        return None
    return obj