#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

sal = pd.read_csv("Data/salinity.csv", names=["sal"])
par = pd.read_csv("Data/par.csv", names=["par"])
pressure = pd.read_csv("Data/pressure.csv", names=["pressure"])
temp = pd.read_csv("Data/temperature.csv", names=["temp"])
time = pd.read_csv("Data/time.csv", names=["time"])

all_props = sal.join([par,pressure,temp,time])
print(all_props.columns)
