from datetime import datetime

def ts_now():
    ts_now = datetime.now().timestamp()
    ts_now = str(ts_now)
    ts_now = int(ts_now.split('.')[0])
    return ts_now