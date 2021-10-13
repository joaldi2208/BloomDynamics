#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

sal = pd.read_csv("Data/salinity.csv", names=["sal"],
                  converters = {"sal":lambda x:[float(i) for i in x.split(";")]})
par = pd.read_csv("Data/par.csv", names=["par"],
                  converters = {"par":lambda x:[float(i) for i in x.split(";")]})
pressure = pd.read_csv("Data/pressure.csv", names=["pressure"],
                       converters = {"pressure":lambda x:[float(i) for i in x.split(";")]})
temp = pd.read_csv("Data/temperature.csv", names=["temp"],
                   converters = {"temp":lambda x:[float(i) for i in x.split(";")]})
time = pd.read_csv("Data/time.csv", names=["time"],
                   converters = {"time":lambda x:[pd.to_datetime(float(i), unit="ns") for i in x.split(";")]})
chloro = pd.read_csv("Data/chlorophyll.csv", names=["chloro"],
                   converters = {"chloro":lambda x:[float(i) for i in x.split(";")]})

all_props = sal.join([par,pressure,temp,time,chloro])

def create_figure(x_values, y_values, color_values, colormap):
    stacked_color_values = np.column_stack((all_props[f"{color_values}"]))
    x_axis_values = x_values[0]
    y_axis_values = [i[0] for i in y_values]
    y_axis_values = np.array([y_axis_values])[0,:]
    fig, ax = plt.subplots()
    plot = plt.pcolormesh(y_axis_values,x_axis_values,stacked_color_values,cmap=f"{colormap}")
    plt.colorbar(plot,label=f"{barlabel}")
    plt.xlabel("Time (d)")
    plt.ylabel("Pressure (dbar)")
    ax.invert_yaxis()
    plt.show()

newPlot = input("Do you want to plot:")
while newPlot == "y":
    variable = input("variable:")
    colormap = input("colormap:")
    barlabel = input("barlabel:")
    create_figure(all_props["pressure"].values, all_props["time"].values, variable, colormap)
    newPlot = input("Do you want to plot:")
