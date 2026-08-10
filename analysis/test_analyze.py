import os, json
import matplotlib.pyplot as plt
import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/')

def b64str_to_12bitIntList(s):
    b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    return [b.index(s[2*i])+b.index(s[2*i+1])*64 for i in range(len(s)//2)]

timestamps = []
values = []
for fname in sorted(os.listdir(DATA_PATH)):
    with open(os.path.join(DATA_PATH, fname), "r") as f:
        data = json.load(f)
    print(data)

    if isinstance(data, list):
        new_timestamps = [entry["unix_timestamp"] for entry in data if "unix_timestamp" in entry]
        new_values = [entry["adc_raw"] for entry in data if "unix_timestamp" in entry]
    elif isinstance(data, dict):
        new_values = b64str_to_12bitIntList(data["data"])
        N = len(new_values)
        dt = (data["tstamp_end"]-data["tstamp_start"])/N
        new_timestamps = [data["tstamp_start"]+dt*i for i in range(N)]
    else:
        raise TypeError(f"invalid type {type(data)}")
    timestamps += new_timestamps
    values += new_values

plt.plot([datetime.datetime.fromtimestamp(t) for t in timestamps], values, ".")
plt.show()
