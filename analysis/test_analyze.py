import os, json
import matplotlib.pyplot as plt
import datetime
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/')

def b64str_to_12bitIntList(s):
    b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    return [b.index(s[2*i])+b.index(s[2*i+1])*64 for i in range(len(s)//2)]

timestamps = []
values = []
for fname in sorted(os.listdir(DATA_PATH)):
    with open(os.path.join(DATA_PATH, fname), "r") as f:
        data = json.load(f)

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

def sliding_window_avg(arr, f, step_size=5, window_length=10, post_map=None):
    if not post_map:
        def post_map(x):
            return x
    return np.array([post_map(f(arr[i:i+window_length]))
        for i in range(0, len(arr)-window_length+1, step_size)])

X = sliding_window_avg(timestamps, np.median, post_map=datetime.datetime.fromtimestamp)
Y = 50.0*sliding_window_avg(values, np.median)*0.001
dates = np.array(
    sorted(set(datetime.datetime.strftime(x, "%Y-%m-%d") for x in X)))

plt.figure(figsize=(12, 3*len(dates)))
for i, d in enumerate(dates):
    plt.subplot(len(dates), 1, i+1)
    dt1 = datetime.datetime.strptime(d, "%Y-%m-%d")
    dt2 = dt1 + datetime.timedelta(days=1)
    mask = np.logical_and(dt1 <= X, X < dt2)
    plt.plot(X[mask], Y[mask], "-", color=(0.0, 0.3, 0.8, 0.7))
    plt.title(d)
    plt.xlabel("Time")
    plt.ylabel("Acoustic\nlevel [dB]")
    plt.xlim((dt1, dt2))
    plt.ylim((35, 65))
    plt.grid()
plt.tight_layout()
plt.show()
