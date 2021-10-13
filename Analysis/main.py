#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sal = pd.read_csv("Data/salinity.csv", names=["sal"], converters = {"sal":lambda x:[float(i) for i in x.split(";")]})
#sal = pd.read_csv("Data/salinity.csv", names=["sal"], converters = {"sal":lambda x:x.split(";")})
par = pd.read_csv("Data/par.csv", names=["par"],converters = {"par":lambda x:[float(i) for i in x.split(";")]})
pressure = pd.read_csv("Data/pressure.csv", names=["pressure"],converters = {"pressure":lambda x:[float(i) for i in x.split(";")]})
temp = pd.read_csv("Data/temperature.csv", names=["temp"],converters = {"temp":lambda x:[float(i) for i in x.split(";")]})
time = pd.read_csv("Data/time.csv", names=["time"],converters = {"time":lambda x:[pd.to_datetime(float(i), unit="ns") for i in x.split(";")]})

all_props = sal.join([par,pressure,temp,time])
exploded_all_props = all_props.explode("sal", ignore_index=True)
print(exploded_all_props)
#fig = plt.figure()
#ax = plt.subplot()

#ax.plot(all_props.time,all_props.sal.values)
#plt.show()

