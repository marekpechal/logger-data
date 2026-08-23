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

    if isinstance(data, dict):
        new_values = b64str_to_12bitIntList(data["data"])
        N = len(new_values)
        T =data["tstamp_end"]-data["tstamp_start"]
        dt = T/N
        new_timestamps = [data["tstamp_start"]+dt*i for i in range(N)]
    else:
        raise TypeError(f"invalid type {type(data)}")

    print(fname, N, T)
