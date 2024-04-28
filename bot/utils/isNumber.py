# tryParseInt

def isNumber(text: str):
    try:
        text = int(text)
        return True
    except:
        return False