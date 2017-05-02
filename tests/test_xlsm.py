# -*- coding: utf-8 -*-
#
#  test_xlsm.py
#  pangaea
#
#  Author : Alan D Snow, 2017.
#  License: BSD 3-Clause

from os import path

from numpy.testing import assert_almost_equal
from osgeo import osr
import pandas as pd
from affine import Affine

import pangaea as pa


def test_read_wrf(tgrid):
    """Test reading in WRF grid"""
    path_to_lsm_files = path.join(tgrid, 'wrf_data', '*.nc')
    lsm_lat_var = 'XLAT'
    lsm_lon_var = 'XLONG'
    lsm_time_dim = 'Time'
    lsm_time_var = 'Times'
    lsm_lat_dim = 'south_north'
    lsm_lon_dim = 'west_east'

    with pa.open_mfdataset(path_to_lsm_files,
                           lat_var=lsm_time_var,
                           lon_var=lsm_lon_var,
                           time_var=lsm_time_var,
                           lat_dim=lsm_lat_dim,
                           lon_dim=lsm_lon_dim,
                           time_dim=lsm_time_dim) as xd:
        # print(xd)
        # make sure coordinates correct
        assert lsm_lat_var in xd.coords
        assert lsm_lon_var in xd.coords
        assert lsm_time_var in xd.coords
        # check @property attributes
        date_array = ['2016-08-23 22:00:00', '2016-08-23 23:00:00',
                      '2016-08-24 00:00:00', '2016-08-24 01:00:00',
                      '2016-08-24 02:00:00', '2016-08-24 03:00:00',
                      '2016-08-24 04:00:00', '2016-08-24 05:00:00',
                      '2016-08-24 06:00:00', '2016-08-24 07:00:00',
                      '2016-08-24 08:00:00', '2016-08-24 09:00:00',
                      '2016-08-24 10:00:00', '2016-08-24 11:00:00',
                      '2016-08-24 12:00:00', '2016-08-24 13:00:00']
        assert (xd.lsm.datetime == pd.to_datetime(date_array)).all()
        # check projection
        proj4_str = ('+proj=lcc +lat_1=35.0600013733 '
                     '+lat_2=35.0600013733 +lat_0=35.060005188 '
                     '+lon_0=-106.599998474 +x_0=0 +y_0=0 +a=6370000 '
                     '+b=6370000 +units=m +no_defs ')
        assert xd.lsm.projection.ExportToProj4() == proj4_str
        # check other attrs
        assert xd.lsm.epsg is None
        assert_almost_equal(xd.lsm.geotransform,
                            (-872999.84920640418, 5999.9997414365271, 0,
                             657001.05737870606, 0, -6000.0006532160332))
        assert_almost_equal(xd.lsm.dx, 5999.9997414365271)
        assert_almost_equal(xd.lsm.dy, 6000.0006532160332)
        assert xd.lsm.affine == Affine.from_gdal(*xd.lsm.geotransform)
        assert xd.lsm.x_size == 288
        assert xd.lsm.y_size == 225
        lat, lon = xd.lsm.latlon
        assert lat.shape == (225, 288)
        assert lon.shape == (225, 288)
        assert_almost_equal(lat[20:23, 145:148],
                            [[39.85745239, 39.85743713, 39.85737228],
                             [39.80366898, 39.80365372, 39.80360413],
                             [39.74989319, 39.74987793, 39.74981308]])
        assert_almost_equal(lon[144:147, 15:17],
                            [[-114.95758057, -114.89360046],
                             [-114.95220947, -114.88827515],
                             [-114.94685364, -114.88293457]])
        y_coords, x_coords = xd.lsm.coords
        assert y_coords.shape == (225, 288)
        assert x_coords.shape == (225, 288)
        assert_almost_equal(x_coords[100:102, 220:223],
                            [[450000.73102539, 456001.01108335, 461999.00957301],
                             [450000.87845214, 455999.62489789, 461998.74249732]])
        assert_almost_equal(y_coords[100:102, 220:223],
                            [[54001.6699001, 54002.25923271, 54001.19124676],
                             [48001.46501146, 48001.3544065, 48001.84096264]])
        assert_almost_equal(xd.lsm.center,
                            (-106.6985855102539, 34.77546691894531))

        # test getvar method
        lrainc = xd.lsm.getvar('RAINC',
                               x_index_start=100,
                               x_index_end=102,
                               y_index_start=200,
                               y_index_end=202)
        rainc = xd['RAINC'][:, 22:24, 100:102][:, ::-1, :]
        assert rainc.equals(lrainc)

        lcldfr = xd.lsm.getvar('CLDFRA',
                               x_index_start=100,
                               x_index_end=102,
                               y_index_start=200,
                               y_index_end=202,
                               calc_4d_method='max',
                               calc_4d_dim='bottom_top')
        cldfr = xd['CLDFRA'][:, :, 22:24, 100:102] \
                    .max(dim='bottom_top')[:, ::-1, :]
        assert cldfr.equals(lcldfr)
