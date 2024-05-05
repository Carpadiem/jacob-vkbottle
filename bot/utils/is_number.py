# tryParseInt

def is_number(text: str):
    try:
        text = int(text)
        return True
    except:
        return False