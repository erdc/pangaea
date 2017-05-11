# -*- coding: utf-8 -*-
#
#  test_xlsm_nwm.py
#  pangaea
#
#  Author : Alan D Snow, 2017.
#  License: BSD 3-Clause

from os import path

from numpy.testing import assert_almost_equal
import pandas as pd
from affine import Affine
import pytest
import xarray as xr

import pangaea as pa

from .conftest import compare_proj4


class NWM(object):
    lsm_lat_var = 'y'
    lsm_lon_var = 'x'
    lsm_time_dim = 'time'
    lsm_time_var = 'time'
    lsm_lat_dim = 'y'
    lsm_lon_dim = 'x'

    def __init__(self, tread, input_folder):
        self.path_to_lsm_files = \
            path.join(tread, input_folder, '*.nc')

    @property
    def xd(self):
        return pa.open_mfdataset(self.path_to_lsm_files,
                                 lat_var=self.lsm_lat_var,
                                 lon_var=self.lsm_lon_var,
                                 time_var=self.lsm_time_var,
                                 lat_dim=self.lsm_lat_dim,
                                 lon_dim=self.lsm_lon_dim,
                                 time_dim=self.lsm_time_dim,
                                 coords_projected=True,
                                 lon_to_180=True)


@pytest.fixture(scope="module")
def nwm(request, tread):
    return NWM(tread, 'nwm_data')


def test_read_nwm(nwm):
    """Test reading in NWM grids"""
    with nwm.xd as xd:
        # make sure coordinates correct
        assert nwm.lsm_lat_var in xd.coords
        assert nwm.lsm_lon_var in xd.coords
        assert nwm.lsm_time_var in xd.coords
        # check @property attributes
        date_array = ['2017-04-19 00:00:00', '2017-04-19 01:00:00']
        assert (xd.lsm.datetime == pd.to_datetime(date_array)).all()
        # check projection
        proj4_str = ('+proj=lcc +lat_1=30 +lat_2=60 +lat_0=40 +lon_0=-97 '
                     '+x_0=0 +y_0=0 +a=6370000 +b=6370000 +units=m +no_defs ')
        compare_proj4(xd.lsm.projection.ExportToProj4(), proj4_str)
        # check other attrs
        assert xd.lsm.epsg is None
        assert_almost_equal(xd.lsm.geotransform,
                            (-2248001.0, 1000.0, 0, -1899000.125, 0, -1000.0),
                            decimal=3)
        assert_almost_equal(xd.lsm.dx, 1000.0)
        assert_almost_equal(xd.lsm.dy, 1000.0)
        assert xd.lsm.affine == Affine.from_gdal(*xd.lsm.geotransform)
        assert xd.lsm.x_size == 6
        assert xd.lsm.y_size == 6
        lat, lon = xd.lsm.latlon
        assert lat.shape == (6, 6)
        assert lon.shape == (6, 6)
        assert_almost_equal(lat,
                            [[20.36527797, 20.36745229, 20.36962574,
                              20.37179832, 20.37397003, 20.37614086],
                             [20.3735187, 20.37569339, 20.3778672,
                              20.38004014, 20.38221221, 20.38438341],
                             [20.38175984, 20.38393489, 20.38610906,
                              20.38828236, 20.39045479, 20.39262635],
                             [20.39000138, 20.39217679, 20.39435133,
                              20.39652499, 20.39869778, 20.40086969],
                             [20.39824332, 20.40041909, 20.40259399,
                              20.40476801, 20.40694116, 20.40911344],
                             [20.40648566, 20.4086618, 20.41083705,
                              20.41301144, 20.41518495, 20.41735759]])
        assert_almost_equal(lon,
                            [[-117.66034789, -117.65155767, -117.64276693,
                              -117.63397569, -117.62518394, -117.61639168],
                             [-117.66266791, -117.65387679, -117.64508515,
                              -117.63629301, -117.62750036, -117.61870721],
                             [-117.66498843, -117.65619641, -117.64740388,
                              -117.63861084, -117.6298173, -117.62102324],
                             [-117.66730947, -117.65851655, -117.64972312,
                              -117.64092918, -117.63213474, -117.62333978],
                             [-117.66963101, -117.6608372, -117.65204287,
                              -117.64324803, -117.63445269, -117.62565683],
                             [-117.67195307, -117.66315835, -117.65436313,
                              -117.64556739, -117.63677115, -117.62797439]])
        y_coords, x_coords = xd.lsm.coords
        assert y_coords.shape == (6, 6)
        assert x_coords.shape == (6, 6)
        assert_almost_equal(y_coords,
                            [[-1899500.125, -1899500.125, -1899500.125,
                              -1899500.125, -1899500.125, -1899500.125],
                             [-1898500.125, -1898500.125, -1898500.125,
                              -1898500.125, -1898500.125, -1898500.125],
                             [-1897500.125, -1897500.125, -1897500.125,
                              -1897500.125, -1897500.125, -1897500.125],
                             [-1896500.125, -1896500.125, -1896500.125,
                              -1896500.125, -1896500.125, -1896500.125],
                             [-1895500.125, -1895500.125, -1895500.125,
                              -1895500.125, -1895500.125, -1895500.125],
                             [-1894500.125, -1894500.125, -1894500.125,
                              -1894500.125, -1894500.125, -1894500.125]])
        assert_almost_equal(x_coords,
                            [[-2247501., -2246501., -2245501.,
                              -2244501., -2243501., -2242501.],
                             [-2247501., -2246501., -2245501.,
                              -2244501., -2243501., -2242501.],
                             [-2247501., -2246501., -2245501.,
                              -2244501., -2243501., -2242501.],
                             [-2247501., -2246501., -2245501.,
                              -2244501., -2243501., -2242501.],
                             [-2247501., -2246501., -2245501.,
                              -2244501., -2243501., -2242501.],
                             [-2247501., -2246501., -2245501.,
                              -2244501., -2243501., -2242501.]])
        assert_almost_equal(xd.lsm.center,
                            (-117.64416675875698, 20.391316307070426))
        # test getvar method
        ltemp = xd.lsm.getvar('T2D')
        temp = xd['T2D']
        assert temp.equals(ltemp)
