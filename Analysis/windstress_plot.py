#!/usr/bin/python3

import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

from mpl_toolkits.axes_grid1 import make_axes_locatable

def wind_stress(fig, ax, wlength=21, porder=3, i=None, num_sub=2):
    ds = xr.open_dataset("Data/windspeed.grib", engine="cfgrib")
    # for v in ds:
    #     print("{}, {}, {}".format(v, ds[v].attrs["long_name"], ds[v].attrs["units"]))

    df_s = ds.to_dataframe()
    df = df_s.groupby(df_s.valid_time).mean()
    df["valid_time"] = df_s.valid_time.unique()
    df["wind"] = (df.u10**2 + df.v10**2).apply(lambda x: x*1.2*(0.001*(1.1+0.035*np.sqrt(x))))
    df = df.iloc[4:219]
    filtered_wind = signal.savgol_filter(df.wind,wlength,porder)

        
    if i != None:
        im = ax[i].plot(df.valid_time, df.wind, "darkorange", label="Raw data")
        im = ax[i].plot(df.valid_time, filtered_wind, "navy", label=f"SG smoothed")
        divider = make_axes_locatable(ax[i])
        cax = divider.append_axes("right", size="3%", pad=0.5)
        cax.axis("off")
        ax[i].set_ylabel("Wind Stress \n [N/m$^2$]", fontsize=13)
        ax[i].set_xlim(df.valid_time[1], df.valid_time[-1])
        ticks = None if num_sub-1 == i else ax[i].set_xticks([])
        ax[i].legend()
    else:
        im = ax.plot(df.valid_time, df.wind, "darkorange", label="Raw data")
        im = ax.plot(df.valid_time, filtered_wind, "navy", label=f"SG smoothed")
        ax.set_xlabel("Days [d]")
        ax.set_ylabel("Wind Stress \n [N/m$^2$]", fontsize=13)
        ax.set_xlim(df.valid_time[1], df.valid_time[-1])
        plt.legend()
    return im
if __name__ == "__main__":
    fig, ax = plt.subplots()
    im = wind_stress(fig, ax)
    plt.show()
