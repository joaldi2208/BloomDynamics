#!/usr/bin/python3

import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from scipy import signal

from mpl_toolkits.axes_grid1 import make_axes_locatable

def wind_stress(fig, ax, wlength=21, porder=3, i=None, num_sub=2):
    ds = xr.open_dataset("Data/windspeed.grib", engine="cfgrib")
    # for v in ds:
    #     print("{}, {}, {}".format(v, ds[v].attrs["long_name"], ds[v].attrs["units"]))

    df = ds.to_dataframe()
    df = df.iloc[4:219]

    filtered_wind = signal.savgol_filter(df.wind,wlength,porder)

    if i != None:
        im = ax[i].plot(df.valid_time, df.wind, "darkorange", label="Raw data")
        im = ax[i].plot(df.valid_time, filtered_wind, "navy", label=f"SG smoothed")
        divider = make_axes_locatable(ax[i])
        cax = divider.append_axes("right", size="3%", pad=0.5)
        cax.axis("off")
        ax[i].set_ylabel("Wind Stress [Pa]")
        ax[i].set_xlim("2021-03-05 08:00:00","2021-10-05 08:00:00")
        ticks = None if num_sub-1 == i else ax[i].set_xticks([])
        ax[i].legend()
    else:
        im = ax.plot(df.valid_time, df.wind, "darkorange", label="Raw data")
        im = ax.plot(df.valid_time, filtered_wind, "navy", label=f"SG smoothed")
        ax.set_xlabel("Days [d]")
        ax.set_ylabel("Wind Stress [Pa]")
        ax.set_xlim("2021-03-05 08:00:00","2021-10-05 08:00:00")
        plt.legend()
    return im
if __name__ == "__main__":
    fig, ax = plt.subplots()
    im = wind_stress(fig, ax)
    plt.show()