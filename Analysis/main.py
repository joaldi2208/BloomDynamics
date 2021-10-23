#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import gsw
import random
import os
import matplotlib.colors as colors

from mpl_toolkits.axes_grid1 import make_axes_locatable

from windstress_plot import wind_stress

chlorophyll_list = []
with open("Data/chlorophyll.csv", "r") as file:
    values = file.readlines()
    for value in values:
        value = value.replace("\n","")
        for sub_value in value.split(";"):
            chlorophyll_list.append(float(sub_value))
min_chloro = np.nanmin(chlorophyll_list)


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
               converters = {"chloro":lambda x:[float(i)+abs(min_chloro) for i in x.split(";")]})

all_props = sal.join([par,pressure,temp,time,chloro])


all_props["density"] = ""
for i in range(len(all_props.sal)):
    all_props["density"][i] = gsw.sigma0(all_props.sal[i],all_props.temp[i])

def create_figure(x_values, y_values, color_values, colormap, values_to_label, i, num_sub,log):
    '''creates a HEATMAP for sal, par, temp, pressure or density. The date is
    plotted on the pressure is plotted on the y-axis.'''
    stacked_color_values = np.column_stack((all_props[f"{color_values}"]))
    x_axis_values = x_values[0]
    y_axis_values = [i[0] for i in y_values]
    y_axis_values = np.array([y_axis_values])[0,:]
    if i == None:
        if log == "log":
            plot = ax.pcolormesh(y_axis_values,x_axis_values,stacked_color_values,cmap=f"{colormap}",norm=colors.LogNorm(), shading="auto")
        else:
            plot = ax.pcolormesh(y_axis_values,x_axis_values,stacked_color_values,cmap=f"{colormap}", shading="auto", 
                    norm=colors.BoundaryNorm(np.linspace(np.nanmin(stacked_color_values),np.nanmax(stacked_color_values),15),ncolors=256))

        ax.invert_yaxis()
        plt.colorbar(plot,label=values_to_label[color_values])
        plt.ylabel("Pressure [dbar]")
        plt.xlabel("Time [d]")
    else:
        if log == "log":
            plot = ax[i].contourf(y_axis_values,x_axis_values,stacked_color_values,cmap=f"{colormap}", norm=colors.LogNorm(), shading="auto")
        else:
            plot = ax[i].contourf(y_axis_values,x_axis_values,stacked_color_values,cmap=f"{colormap}", shading="auto", 
                    norm=colors.BoundaryNorm(np.linspace(np.nanmin(stacked_color_values),np.nanmax(stacked_color_values),15),ncolors=256))

        ax[i].invert_yaxis()
        divider = make_axes_locatable(ax[i])
        cax = divider.append_axes("right", size="3%", pad=0.5)
        fig.colorbar(plot, cax=cax, ax=ax[i], label=values_to_label[color_values], orientation="vertical")
        ticks = None if num_sub-1 == i else ax[i].set_xticks([])
        ax[i].set_ylabel("Pressure [dbar]")
    
    


def figure_layout(answer):
    values_to_label = {"density":"Density [kg/m$^3$]", "chloro":"Chlorophyll [$\mu q$/L]", "temp":"Temperatur [$^\circ$C]", "par":"PAR [$\mu q/cm² nm¹$]", "sal":"Salinity PSU", "wind":"Wind Stress [Pa]","par log":"PAR [$\mu q/cm² nm¹$]","chloro log":"Chlorophyll [$\mu g$/L]"}
    print("******************************** \n")
    for name_pair in values_to_label.items():
        print(f"{name_pair[0]} --> {name_pair[1]}")
    print("******************************** \n")
    global fig, ax
    if answer == "y":
        fig, ax = plt.subplots()
        i, num_sub = None, None
        variable, colormap, im, log = choose_variable(i, num_sub)
        if variable != "wind":
            create_figure(all_props["pressure"].values, all_props["time"].values, variable, colormap, values_to_label, None, None, log)
        plt.show()
    elif answer == "a":
        num_sub = int(input("Number of subplots:"))
        fig, ax = plt.subplots(num_sub)
        plt.subplots_adjust(hspace=0.1)
        ax = ax.ravel()
        for i in range(num_sub):
            variable, colormap, im, log = choose_variable(i, num_sub)
            if variable == "wind":
                pass
            else:    
                create_figure(all_props["pressure"].values, all_props["time"].values, variable, colormap, values_to_label, i, num_sub, log)
        ax[i].set_xlabel("Time [d]")
        plt.show()

    
def choose_variable(i, num_sub):
    variable = input("variable:")
    try:
        variable, log = variable.split(" ")
    except ValueError:
        log = None
    im, colormap = None, None
    if variable == "wind":
        wlength = input("Window Length !!must be an ODD number!! [default 21 -> press ENTER]:")
        porder = input("Polynom Order [default 3 -> press ENTER]:")
        if wlength == "" and porder == "":
            im = wind_stress(fig, ax,21,3,i=i, num_sub=num_sub)
        elif wlength != "" and porder == "":
            im = wind_stress(fig, ax, wlength=int(wlength),porder=3,i=i,num_sub=num_sub)
        elif wlength == "" and porder != "":
            im = wind_stress(fig, ax,21, int(porder),i=i,num_sub=num_sub)
        elif wlength != "" and porder != "":
            im = wind_stress(fig, ax,int(wlength), int(porder),i=i,num_sub=num_sub)
    else:
        colormap = input("colormap:")
    return variable, colormap, im, log


if __name__ == "__main__":
    try:
        path_list = os.listdir("/Users/")
        names = ["onas","ulia","lma","aria","ugusta"]
        names_list = [name_in_path for name_in_path in path_list for name in names if name in name_in_path]
        print("\t \t \t --------------")
        print(f"\t \t \t | hello {names_list[0]} |")
        print("\t \t \t --------------")
    except IndexError and FileNotFoundError:
        print("\t \t \t --------------")
        print("\t \t \t | hello |")
        print("\t \t \t --------------")
    print("\t This program allow you several different options for plots")
    print("\t There is a single plot mode [y] and an advanced mode for multiple plots [a]")
    print("\t Press anything else to exit the program \n ")
    newPlot = input("Which plot-mode you want to use[y][a][n]:")
    while newPlot == "y" or newPlot == "a":
        figure_layout(newPlot)
        newPlot = input("Which plot-mode you want to use[y][a][n]:")





