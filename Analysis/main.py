#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import gsw
import random
import os
import matplotlib.colors as colors
import cmocean.cm as cmo

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

# density column
all_props["density"] = ""
all_props["nsquared"] = ""
for i in range(len(all_props.sal)):
    all_props["density"][i] = gsw.sigma0(all_props.sal[i],all_props.temp[i])
    all_props["nsquared"][i] = gsw.Nsquared(all_props.sal[i],all_props.temp[i],all_props.pressure[i])

all_props["nsquared1"] = ""
all_props["nsquared2"] = ""
for i in range(len(all_props.nsquared)):
    all_props["nsquared1"][i] = all_props.nsquared[i][0]*1000
    all_props["nsquared2"][i] = all_props.nsquared[i][1]

# Nsquare
# def nsquared():


# mixed layer depth calculation
# mixed_layer_depth_calculation():
mld_list = []
for index, value_list in enumerate(all_props.density):
    one_date_list = []
    for index2, value in enumerate(value_list):
        if all_props.pressure[index][index2] < 4:
            one_date_list.append(value)
    mld_list.append(np.nanmean(one_date_list)+0.125)

mld = []
for index, value_list in enumerate(all_props.pressure):
    one_date_list = []
    for index2, value in enumerate(value_list):
        if all_props.density[index][index2] < mld_list[index]:
            one_date_list.append(value)
    try:
        mld.append(np.nanmax(one_date_list))
    except ValueError:
        mld.append(np.nan) 
            
# euphotic depth calculation
# euphotic_deph_calculation():
ezd = []
for value_list in all_props.par:
    try:
        max_value = np.nanmax(value_list)
        ezd.append(max_value*0.01)
    except ValueError:
        ezd.append(np.nan)
        
# functions


def create_figure(x_values, y_values, color_values, colormap, values_to_label, i, num_sub,log):
    '''creates a HEATMAP for sal, par, temp, pressure or density. The date is
    plotted on the pressure is plotted on the y-axis.'''
    stacked_color_values = np.column_stack((all_props[f"{color_values}"]))
    x_axis_values = x_values[0]
    y_axis_values = [i[0] for i in y_values]
    y_axis_values = np.array([y_axis_values])[0,:]

    if i == None:
        if log == "log":
            plot = ax.pcolormesh(y_axis_values,x_axis_values,stacked_color_values,cmap=f"cmo.{colormap}",norm=colors.LogNorm(), shading="auto")
            cb = plt.colorbar(plot)
        else:
            plot = ax.pcolormesh(y_axis_values,x_axis_values,stacked_color_values,cmap=f"cmo.{colormap}", shading="auto", 
                    norm=colors.BoundaryNorm(np.linspace(np.nanmin(stacked_color_values),np.nanmax(stacked_color_values),50),ncolors=256))
            cb = plt.colorbar(plot)
            cb.set_ticks(np.arange(int(np.nanmin(stacked_color_values)),
                int(np.nanmax(stacked_color_values)*1.1),
                2))
        if log == "layers":
            mldr_plot = ax.plot(y_axis_values, mld, "cyan", label="MLD", linewidth=0.5)
            ezd_plot = ax.plot(y_axis_values, ezd, "magenta", label="EZD", linewidth=0.5)
            legend = ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)

        ax.invert_yaxis()
        #plt.colorbar(plot,label=values_to_label[color_values])
        cb.set_label(label=values_to_label[color_values], size="x-large")
        plt.ylabel("Pressure \n [dbar]", fontsize=15)
        plt.xlabel("Time [d]", fontsize=15)
    else:
        if log == "log":
            plot = ax[i].pcolormesh(y_axis_values,x_axis_values,stacked_color_values,cmap=f"cmo.{colormap}", norm=colors.LogNorm(),shading="auto")
            divider = make_axes_locatable(ax[i])
            cax = divider.append_axes("right", size="3%", pad=0.5)
            cb = plt.colorbar(plot, cax=cax, ax=ax[i])
        else:
            plot = ax[i].pcolormesh(y_axis_values,x_axis_values,stacked_color_values,cmap=f"cmo.{colormap}", shading="auto", 
                    norm=colors.BoundaryNorm(np.linspace(np.nanmin(stacked_color_values),np.nanmax(stacked_color_values),50),ncolors=256))
            divider = make_axes_locatable(ax[i])
            cax = divider.append_axes("right", size="3%", pad=0.5)
            cb = plt.colorbar(plot, cax=cax, ax=ax[i])
            cb.set_ticks(np.arange(int(np.nanmin(stacked_color_values)),
            int(np.nanmax(stacked_color_values)*1.1),
            2))
            print(np.nanmin(stacked_color_values),np.nanmax(stacked_color_values))
            
        if log == "layers":
            mldr_plot = ax[i].plot(y_axis_values, mld, "cyan", label="MLD", linewidth=0.5)
            ezd_plot = ax[i].plot(y_axis_values, ezd, "magenta", label="EZD", linewidth=0.5)
            legend = ax[i].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)
            #legend.get_frame().set_facecolor('C0')
        ax[i].invert_yaxis()
        #fig.colorbar(plot, cax=cax, ax=ax[i], label=values_to_label[color_values], orientation="vertical")
        cb.set_label(label=values_to_label[color_values], size="x-large")
        ticks = None if num_sub-1 == i else ax[i].set_xticks([])
        ax[i].set_ylabel("Pressure \n [dbar]", fontsize=15)
    
    


def figure_layout(answer):
    values_to_label = {"density":"Density \n [kg/m$^3$]", "chloro":"Chlorophyll \n [$\mu q$/L]", "temp":"Temperatur \n [$^\circ$C]", "par":"PAR \n [$\mu q/cm?? nm??$]", "sal":"Salinity \n PSU", "wind":"Wind Stress \n [Pa]","par log":"PAR \n [$\mu q/cm?? nm??$]","chloro \n log":"Chlorophyll [$\mu g$/L]","nsquared1": "N$^2$ \n [rad$^2$/s$^2\cdot 10^3$]"}
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
        ax[i].set_xlabel("Time [d]",fontsize=15)
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





