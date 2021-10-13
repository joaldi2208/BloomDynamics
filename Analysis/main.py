#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import gsw

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

all_props["density"] = ""
for i in range(len(all_props.sal)):
    all_props["density"][i] = gsw.sigma0(all_props.sal[i],all_props.temp[i])


def create_figure(x_values, y_values, color_values, colormap, values_to_label):
    '''creates a HEATMAP for sal, par, temp, pressure or density. The date is
    plotted on the pressure is plotted on the y-axis.'''
    stacked_color_values = np.column_stack((all_props[f"{color_values}"]))
    x_axis_values = x_values[0]
    y_axis_values = [i[0] for i in y_values]
    y_axis_values = np.array([y_axis_values])[0,:]
    fig, ax = plt.subplots()
    plot = plt.pcolormesh(y_axis_values,x_axis_values,stacked_color_values,cmap=f"{colormap}")
    plt.colorbar(plot,label=values_to_label[color_values])
    plt.xlabel("Time [d]")
    plt.ylabel("Pressure [dbar]")
    ax.invert_yaxis()
    plt.show()

if __name__ == "__main__":
    values_to_label = {"density":"Density [g/cm$^3$]", "chloro":"Chlorophyll [mg/L]", "temp":"Temperatur [$^\circ$C]", "par":"Photosynthetically Active Radiation [PPF]", "sal":"Salinity [g/kg]" }
    newPlot = input("Do you want to plot:")
    while newPlot == "y":
        for name_pair in values_to_label.items():
            print(f"{name_pair[0]} --> {name_pair[1]}")
        variable = input("variable:")
        colormap = input("colormap:")
        create_figure(all_props["pressure"].values, all_props["time"].values, variable, colormap, values_to_label)
        newPlot = input("Do you want to plot:")
