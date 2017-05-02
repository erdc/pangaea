# -*- coding: utf-8 -*-
#
#  read.py
#  pangaea
#
#  Author : Alan D Snow, 2017.
#  License: BSD 3-Clause

import xarray as xr


def open_mfdataset(path_to_lsm_files,
                   lat_var,
                   lon_var,
                   time_var,
                   lat_dim,
                   lon_dim,
                   time_dim,
                   autoclose=True,
                   ):

    def define_coords(ds):
        """xarray loader to ensure coordinates are loaded correctly"""
        # remove time dimension from lat, lon coordinates
        if ds[lat_var].ndim == 3:
            ds[lat_var] = ds[lat_var].squeeze(time_dim)
        if ds[lon_var].ndim == 3:
            ds[lon_var] = ds[lon_var].squeeze(time_dim)
        # make sure coords are defined as coords
        if lat_var not in ds.coords \
                or lon_var not in ds.coords \
                or time_var not in ds.coords:
            ds.set_coords([lat_var, lon_var, time_var],
                          inplace=True)
        return ds

    xd = xr.open_mfdataset(path_to_lsm_files,
                           autoclose=autoclose,
                           preprocess=define_coords,
                           concat_dim=time_dim)
    xd.lsm.y_var = lat_var
    xd.lsm.x_var = lon_var
    xd.lsm.time_var = time_var
    xd.lsm.y_dim = lat_dim
    xd.lsm.x_dim = lon_dim
    xd.lsm.time_dim = time_dim
    xd.lsm.to_datetime()

    return xd
