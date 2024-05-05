def dict_contains(source: dict, my: dict):
    return all(source.get(k) == v for k, v in my.items())