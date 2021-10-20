#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import gsw
import random
import os


from mpl_toolkits.axes_grid1 import make_axes_locatable

from windstress_plot import wind_stress

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

all_props["log_par"] = ""
all_props["log_chloro"] = ""
all_props["density"] = ""
for i in range(len(all_props.sal)):
    all_props["density"][i] = gsw.sigma0(all_props.sal[i],all_props.temp[i])
    # print(all_props.chloro[i])
    # nan's zu 100 um später zu löschen
    # log_chloro
    no_nan_chloro = np.nan_to_num(all_props.chloro[i], nan=100)
    # negative werte zu eins damit sie 0 werden
    no_nan_chloro = np.where(no_nan_chloro<=0, 1000, no_nan_chloro)
    log_values_chloro = np.log(no_nan_chloro)
    #print(no_nan_chloro)
    #print(log_values_chloro)
    log_values_chloro = np.where(log_values_chloro==np.log(1000), np.nan, log_values_chloro)
    all_props["log_chloro"][i] = np.where(log_values_chloro==np.log(100), np.nan, log_values_chloro)

    # log_par
    no_nan_par = np.nan_to_num(all_props.par[i], nan=10000)
    no_nan_par = np.where(no_nan_par<=0, 100000, no_nan_par)
    log_values_par = np.log(no_nan_par)
    log_values_par = np.where(log_values_par==np.log(100000), np.nan, log_values_par)
    all_props["log_par"][i] = np.where(log_values_par==np.log(10000), np.nan, log_values_par)


    
def create_figure(x_values, y_values, color_values, colormap, values_to_label, i, num_sub):
    '''creates a HEATMAP for sal, par, temp, pressure or density. The date is
    plotted on the pressure is plotted on the y-axis.'''
    stacked_color_values = np.column_stack((all_props[f"{color_values}"]))
    x_axis_values = x_values[0]
    y_axis_values = [i[0] for i in y_values]
    y_axis_values = np.array([y_axis_values])[0,:]
    if i == None:
        plot = ax.pcolormesh(y_axis_values,x_axis_values,stacked_color_values,cmap=f"{colormap}")
        ax.invert_yaxis()
        plt.colorbar(plot,label=values_to_label[color_values])
        plt.ylabel("Pressure [dbar]")
        plt.xlabel("Time [d]")
    else:
        plot = ax[i].contourf(y_axis_values,x_axis_values,stacked_color_values,cmap=f"{colormap}")
        ax[i].invert_yaxis()
        divider = make_axes_locatable(ax[i])
        cax = divider.append_axes("right", size="3%", pad=0.5)
        fig.colorbar(plot, cax=cax, ax=ax[i], label=values_to_label[color_values], orientation="vertical")
        ticks = None if num_sub-1 == i else ax[i].set_xticks([])
        ax[i].set_ylabel("Pressure [dbar]")
    
    


def figure_layout(answer):
    values_to_label = {"density":"Density [kg/m$^3$]", "chloro":"Chlorophyll [$\mu q$/L]", "temp":"Temperatur [$^\circ$C]", "par":"Photo. Active \n Radiation \n [$\mu q/cm² nm¹$]", "sal":"Salinity PSU", "wind":"Wind Stress [Pa]","log_par":"log PAR[$\mu q/cm² nm¹$]","log_chloro":"Chlorophyll log [$\mu q$/L]"}
    print("******************************** \n")
    for name_pair in values_to_label.items():
        print(f"{name_pair[0]} --> {name_pair[1]}")
    print("******************************** \n")
    global fig, ax
    if answer == "y":
        fig, ax = plt.subplots()
        i, num_sub = None, None
        variable, colormap, im = choose_variable(i, num_sub)
        if variable != "wind":
            create_figure(all_props["pressure"].values, all_props["time"].values, variable, colormap, values_to_label, None, None)
        plt.show()
    elif answer == "a":
        num_sub = int(input("Number of subplots:"))
        fig, ax = plt.subplots(num_sub)
        plt.subplots_adjust(hspace=0.1)
        ax = ax.ravel()
        for i in range(num_sub):
            variable, colormap, im = choose_variable(i, num_sub)
            if variable == "wind":
                pass
            else:    
                create_figure(all_props["pressure"].values, all_props["time"].values, variable, colormap, values_to_label, i, num_sub)
        ax[i].set_xlabel("Time [d]")
        plt.show()

    
def choose_variable(i, num_sub):
    variable = input("variable:")
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
    return variable, colormap, im 


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





