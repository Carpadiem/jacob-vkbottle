def isSubset(a: list, b: list):
    for aitem in a:
        for bitem in b:
            if aitem in b:
                break
            else:
                return False
    return True