# -*- coding: utf-8 -*-
#
#  test_xlsm_era.py
#  pangaea
#
#  Author : Alan D Snow, 2017.
#  License: BSD 3-Clause

from os import path

from numpy.testing import assert_almost_equal
import pandas as pd
from affine import Affine
import pytest

import pangaea as pa

from .conftest import compare_proj4

pa.log_to_console(level='DEBUG')

class ERA(object):
    lsm_lat_var = 'latitude'
    lsm_lon_var = 'longitude'
    lsm_time_dim = 'time'
    lsm_time_var = 'time'
    lsm_lat_dim = 'latitude'
    lsm_lon_dim = 'longitude'

    def __init__(self, tread, grid_name):
        self.grid_name = grid_name
        self.path_to_lsm_files = \
            path.join(tread, '{0}_data'.format(grid_name), '*.nc')

    @property
    def xd(self):
        return pa.open_mfdataset(self.path_to_lsm_files,
                                 lat_var=self.lsm_lat_var,
                                 lon_var=self.lsm_lon_var,
                                 time_var=self.lsm_time_var,
                                 lat_dim=self.lsm_lat_dim,
                                 lon_dim=self.lsm_lon_dim,
                                 time_dim=self.lsm_time_dim,
                                 lon_to_180=True)


@pytest.fixture(scope="module", params=["erai"])
def era(request, tread):
    return ERA(tread, request.param)


def test_read_era(era):
    """Test reading in ERA Interim grids"""
    with era.xd as xd:
        # make sure coordinates correct
        assert era.lsm_lat_var in xd.coords
        assert era.lsm_lon_var in xd.coords
        assert era.lsm_time_var in xd.coords
        # check @property attributes
        date_array = ['2016-01-02 00:00:00', '2016-01-02 03:00:00',
                      '2016-01-02 06:00:00', '2016-01-02 09:00:00',
                      '2016-01-02 12:00:00', '2016-01-02 15:00:00',
                      '2016-01-02 18:00:00', '2016-01-02 21:00:00',
                      '2016-01-03 00:00:00', '2016-01-03 03:00:00',
                      '2016-01-03 06:00:00', '2016-01-03 09:00:00',
                      '2016-01-03 12:00:00', '2016-01-03 15:00:00',
                      '2016-01-03 18:00:00', '2016-01-03 21:00:00',
                      '2016-01-04 00:00:00', '2016-01-04 03:00:00',
                      '2016-01-04 06:00:00', '2016-01-04 09:00:00',
                      '2016-01-04 12:00:00', '2016-01-04 15:00:00',
                      '2016-01-04 18:00:00', '2016-01-04 21:00:00',
                      '2016-01-05 00:00:00']
        assert (xd.lsm.datetime == pd.to_datetime(date_array)).all()
        # check projection
        proj4_str = ('+proj=longlat +datum=WGS84 +no_defs ')
        compare_proj4(xd.lsm.projection.ExportToProj4(), proj4_str)
        # check other attrs
        assert xd.lsm.epsg == '4326'
        assert_almost_equal(xd.lsm.geotransform,
                            [-113.25, 0.5, 0, 41.75, 0, -0.5],
                            decimal=3)
        assert_almost_equal(xd.lsm.dx, 0.5)
        assert_almost_equal(xd.lsm.dy, 0.5)
        assert xd.lsm.affine == Affine.from_gdal(*xd.lsm.geotransform)
        assert xd.lsm.x_size == 6
        assert xd.lsm.y_size == 6
        lat, lon = xd.lsm.latlon
        assert lat.shape == (6, 6)
        assert lon.shape == (6, 6)
        assert_almost_equal(lat,
                            [[41.5, 41.5, 41.5, 41.5, 41.5, 41.5],
                             [41., 41., 41., 41., 41., 41.],
                             [40.5, 40.5, 40.5, 40.5, 40.5, 40.5],
                             [40., 40., 40., 40., 40., 40.],
                             [39.5, 39.5, 39.5, 39.5, 39.5, 39.5],
                             [39., 39., 39., 39., 39., 39.]])
        assert_almost_equal(lon,
                            [[-113., -112.5, -112., -111.5, -111., -110.5],
                             [-113., -112.5, -112., -111.5, -111., -110.5],
                             [-113., -112.5, -112., -111.5, -111., -110.5],
                             [-113., -112.5, -112., -111.5, -111., -110.5],
                             [-113., -112.5, -112., -111.5, -111., -110.5],
                             [-113., -112.5, -112., -111.5, -111., -110.5]])
        y_coords, x_coords = xd.lsm.coords
        assert y_coords.shape == (6, 6)
        assert x_coords.shape == (6, 6)
        assert_almost_equal(y_coords,
                            [[41.5, 41.5, 41.5, 41.5, 41.5, 41.5],
                             [41., 41., 41., 41., 41., 41.],
                             [40.5, 40.5, 40.5, 40.5, 40.5, 40.5],
                             [40., 40., 40., 40., 40., 40.],
                             [39.5, 39.5, 39.5, 39.5, 39.5, 39.5],
                             [39., 39., 39., 39., 39., 39.]],
                            decimal=4)
        assert_almost_equal(x_coords,
                            [[-113., -112.5, -112., -111.5, -111., -110.5],
                             [-113., -112.5, -112., -111.5, -111., -110.5],
                             [-113., -112.5, -112., -111.5, -111., -110.5],
                             [-113., -112.5, -112., -111.5, -111., -110.5],
                             [-113., -112.5, -112., -111.5, -111., -110.5],
                             [-113., -112.5, -112., -111.5, -111., -110.5]],
                            decimal=4)
        assert_almost_equal(xd.lsm.center,
                            (-111.75, 40.25))
        # test getvar method
        lrainc = xd.lsm.getvar('tp')
        rainc = xd['tp']
        assert rainc.equals(lrainc)
