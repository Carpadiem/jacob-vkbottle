from datetime import datetime

def ts2date(ts: int):
    date_from_ts = str(datetime.fromtimestamp(ts))
    date_from_ts = date_from_ts.replace('-', '.')
    return date_from_ts