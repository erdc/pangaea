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

from .conftest import compare_proj4, compare_rasters

class ERA(object):
    lsm_lat_var = 'latitude'
    lsm_lon_var = 'longitude'
    lsm_time_dim = 'time'
    lsm_time_var = 'time'
    lsm_lat_dim = 'latitude'
    lsm_lon_dim = 'longitude'

    def __init__(self, tread, data_type):
        self.path_to_lsm_files = \
            path.join(tread, '{0}_data'.format(data_type), '*.nc')

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


@pytest.fixture(scope="module")
def erai(request, tread):
    return ERA(tread, 'erai')


@pytest.fixture(scope="module")
def era5(request, tread):
    return ERA(tread, 'era5')


def test_read_erai(erai):
    """Test reading in ERA Interim grid"""
    with erai.xd as xd:
        # make sure coordinates correct
        assert erai.lsm_lat_var in xd.coords
        assert erai.lsm_lon_var in xd.coords
        assert erai.lsm_time_var in xd.coords
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
