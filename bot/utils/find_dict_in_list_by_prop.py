def find_dict_in_list_by_prop(search_in: list, where: dict):

    # prop_by_id = list(filter(lambda item: item['id'] == prop_id, game_property[category]))[0]

    w_key = list(where.keys())[0]
    w_value = list(where.values())[0]

    obj = list(filter(lambda item: item[w_key] == w_value, search_in))[0]
    return obj