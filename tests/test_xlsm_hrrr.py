# -*- coding: utf-8 -*-
#
#  test_xlsm_hrrr.py
#  pangaea
#
#  Author : Alan D Snow, 2017.
#  License: BSD 3-Clause

import os
from os import path
import sys

from numpy.testing import assert_almost_equal
import pandas as pd
from affine import Affine
import pytest

import pangaea as pa

from .conftest import compare_proj4

pa.log_to_console()


class HRRR(object):
    lsm_lat_var = 'gridlat_0'
    lsm_lon_var = 'gridlon_0'
    lsm_time_dim = 'time'
    lsm_time_var = 'time'
    lsm_lat_dim = 'ygrid_0'
    lsm_lon_dim = 'xgrid_0'

    def __init__(self, tread):
        self.path_to_lsm_files = \
            path.join(tread, 'hrrr_data', '*.grib2')

    @property
    def xd(self):
        return pa.open_mfdataset(self.path_to_lsm_files,
                                 lat_var=self.lsm_lat_var,
                                 lon_var=self.lsm_lon_var,
                                 time_var=self.lsm_time_var,
                                 lat_dim=self.lsm_lat_dim,
                                 lon_dim=self.lsm_lon_dim,
                                 time_dim=self.lsm_time_dim,
                                 loader='hrrr')


@pytest.fixture(scope="module")
def hrrr(request, tread):
    return HRRR(tread)


@pytest.mark.skipif(sys.version_info > (3, 0),
                    reason="pynio only works on Python 2")
@pytest.mark.skipif(os.name == 'nt',
                    reason="pynio not available on Windows")
def test_read_hrrr(hrrr):
    """Test reading in hrrr grids"""
    with hrrr.xd as xd:
        # make sure coordinates correct
        assert hrrr.lsm_lat_var in xd.coords
        assert hrrr.lsm_lon_var in xd.coords
        assert hrrr.lsm_time_var in xd.coords
        # check @property attributes
        date_array = ['2016-09-14 01:00:00', '2016-09-14 02:00:00',
                      '2016-09-14 03:00:00', '2016-09-14 04:00:00',
                      '2016-09-14 05:00:00', '2016-09-14 06:00:00',
                      '2016-09-14 07:00:00', '2016-09-14 08:00:00',
                      '2016-09-14 09:00:00', '2016-09-14 10:00:00',
                      '2016-09-14 11:00:00', '2016-09-14 12:00:00',
                      '2016-09-14 13:00:00', '2016-09-14 14:00:00',
                      '2016-09-14 15:00:00', '2016-09-14 16:00:00',
                      '2016-09-14 17:00:00', '2016-09-14 18:00:00',
                      '2016-09-14 19:00:00']
        assert (xd.lsm.datetime == pd.to_datetime(date_array)).all()
        # check projection
        proj4_str = ('+proj=lcc +lat_1=38.5 +lat_2=38.5 '
                     '+lat_0=40.4941864014 +lon_0=262.5 '
                     '+x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs')
        compare_proj4(xd.lsm.projection.ExportToProj4(), proj4_str)
        # check other attrs
        assert xd.lsm.epsg is None
        assert_almost_equal(xd.lsm.geotransform,
                            [-1232121.72, 3007.225, 0.,
                             151572.681, 0., -2996.084],
                            decimal=3)
        assert_almost_equal(xd.lsm.dx, 3007.2254933631671)
        assert_almost_equal(xd.lsm.dy, 2996.0838590023741)
        assert xd.lsm.affine == Affine.from_gdal(*xd.lsm.geotransform)
        assert xd.lsm.x_size == 33
        assert xd.lsm.y_size == 41
        lat, lon = xd.lsm.latlon
        assert lat.shape == (41, 33)
        assert lon.shape == (41, 33)
        assert_almost_equal(lat[34:36, 27:29],
                            [[40.1655922, 40.1695404],
                             [40.138916, 40.1428604]])
        assert_almost_equal(lon[34:36, 27:29],
                            [[-111.0352097, -111.0002975],
                             [-111.0300446, -110.9951477]])
        y_coords, x_coords = xd.lsm.coords
        assert y_coords.shape == (41, 33)
        assert x_coords.shape == (41, 33)
        assert_almost_equal(y_coords[34:36, 27:29],
                            [[48158.6054, 48157.0677],
                             [45162.7833, 45161.013 ]],
                            decimal=4)
        assert_almost_equal(x_coords[34:36, 27:29],
                            [[-1149362.9558, -1146355.5589],
                             [-1149361.5639, -1146354.4049]],
                            decimal=4)
        assert_almost_equal(xd.lsm.center,
                            [-111.4938354, 40.4941864])
        # test getvar method
        lrhum = xd.lsm.getvar('RH_P0_L103_GLC0')
        rhum = xd['RH_P0_L103_GLC0'][:, ::-1]
        assert rhum.equals(lrhum)
