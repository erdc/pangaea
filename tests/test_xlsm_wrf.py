# -*- coding: utf-8 -*-
#
#  test_xlsm_wrf.py
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

pa.log_to_console(False)

class WRF(object):
    lsm_lat_var = 'XLAT'
    lsm_lon_var = 'XLONG'
    lsm_time_dim = 'Time'
    lsm_time_var = 'Times'
    lsm_lat_dim = 'south_north'
    lsm_lon_dim = 'west_east'

    def __init__(self, tread):
        self.path_to_lsm_files = path.join(tread, 'wrf_data', '*.nc')

    @property
    def xd(self):
        return pa.open_mfdataset(self.path_to_lsm_files,
                                 lat_var=self.lsm_lat_var,
                                 lon_var=self.lsm_lon_var,
                                 time_var=self.lsm_time_var,
                                 lat_dim=self.lsm_lat_dim,
                                 lon_dim=self.lsm_lon_dim,
                                 time_dim=self.lsm_time_dim)


@pytest.fixture(scope="module")
def wrf(request, tread):
    return WRF(tread)


def test_read_wrf(wrf):
    """Test reading in WRF grid"""
    with wrf.xd as xd:
        # make sure coordinates correct
        assert wrf.lsm_lat_var in xd.coords
        assert wrf.lsm_lon_var in xd.coords
        assert wrf.lsm_time_var in xd.coords
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
        compare_proj4(xd.lsm.projection.ExportToProj4(), proj4_str)
        # check other attrs
        assert xd.lsm.epsg is None
        assert_almost_equal(xd.lsm.geotransform,
                            (-872999.84920640418, 5999.9997414365271, 0,
                             657001.05737870606, 0, -6000.0006532160332),
                            decimal=3)
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
                            [[450000.73102539,
                              456001.01108335,
                              461999.00957301],
                             [450000.87845214,
                              455999.62489789,
                              461998.74249732]],
                            decimal=4)
        assert_almost_equal(y_coords[100:102, 220:223],
                            [[54001.6699001,
                              54002.25923271,
                              54001.19124676],
                             [48001.46501146,
                              48001.3544065,
                              48001.84096264]],
                            decimal=4)
        assert_almost_equal(xd.lsm.center,
                            (-106.6985855102539, 34.77546691894531))

        # test getvar method
        lrainc = xd.lsm.getvar('RAINC',
                               x_index_start=100,
                               x_index_end=102,
                               y_index_start=200,
                               y_index_end=202)
        rainc = xd['RAINC'][:, 23:25, 100:102][:, ::-1]
        print(lrainc)
        print(rainc)
        assert rainc.equals(lrainc)

        lcldfr = xd.lsm.getvar('CLDFRA',
                               x_index_start=100,
                               x_index_end=102,
                               y_index_start=200,
                               y_index_end=202,
                               calc_4d_method='max',
                               calc_4d_dim='bottom_top')
        cldfr = xd['CLDFRA'][:, :, ::-1][:, :, 200:202, 100:102] \
            .max(dim='bottom_top')
        assert cldfr.equals(lcldfr)


def test_wrf_tiff(wrf, tgrid):
    """Test write wrf grid"""
    new_raster = path.join(tgrid.output, 'wrf_rainc.tif')
    with wrf.xd as xd:
        xd.lsm.to_tif('RAINC', 3, new_raster)

    compare_rasters(path.join(tgrid.compare, 'wrf_rainc.tif'), new_raster)


def test_wrf_project(wrf):
    """Test project wrf grid"""
    with wrf.xd as xd:
        pgrid = xd.lsm.to_utm('RAINC')
        # make sure coordinates correct
        assert 'lat' in pgrid.coords
        assert 'lon' in pgrid.coords
        assert 'time' in pgrid.coords
        # check @property attributes
        date_array = ['2016-08-23 22:00:00', '2016-08-23 23:00:00',
                      '2016-08-24 00:00:00', '2016-08-24 01:00:00',
                      '2016-08-24 02:00:00', '2016-08-24 03:00:00',
                      '2016-08-24 04:00:00', '2016-08-24 05:00:00',
                      '2016-08-24 06:00:00', '2016-08-24 07:00:00',
                      '2016-08-24 08:00:00', '2016-08-24 09:00:00',
                      '2016-08-24 10:00:00', '2016-08-24 11:00:00',
                      '2016-08-24 12:00:00', '2016-08-24 13:00:00']
        assert (pgrid.lsm.datetime == pd.to_datetime(date_array)).all()
        # check projection
        proj4_str = ('+proj=utm +zone=13 +datum=WGS84 +units=m +no_defs ')
        compare_proj4(pgrid.lsm.projection.ExportToProj4(), proj4_str)
        # check other attrs
        assert pgrid.lsm.epsg == '32613'
        assert_almost_equal(pgrid.lsm.geotransform,
                            [-529776.2885911233, 6010.014137057385, 0.0,
                             4558039.843039687, 0.0, -6010.014137057385],
                            decimal=3)
        assert_almost_equal(pgrid.lsm.dx, 6010.014137057385)
        assert_almost_equal(pgrid.lsm.dy, 6010.014137057385)
        assert pgrid.lsm.affine == Affine.from_gdal(*pgrid.lsm.geotransform)
        assert pgrid.lsm.x_size == 291
        assert pgrid.lsm.y_size == 230
        lat, lon = pgrid.lsm.latlon
        assert lat.shape == (230, 291)
        assert lon.shape == (230, 291)
        assert_almost_equal(lat[20:23, 145:148],
                            [[40.0494547, 40.0505404, 40.0515833],
                             [39.9953332, 39.9964168, 39.9974578],
                             [39.9412112, 39.9422928, 39.9433317]])
        assert_almost_equal(lon[144:147, 15:17],
                            [[-114.9990177, -114.9356954],
                             [-114.9929548, -114.9296693],
                             [-114.9869079, -114.9236591]])
        y_coords, x_coords = pgrid.lsm.coords
        assert y_coords.shape == (230, 291)
        assert x_coords.shape == (230, 291)
        assert_almost_equal(x_coords[100:102, 220:223],
                            [[795431.8286,
                              801441.8428,
                              807451.8569],
                             [795431.8286,
                              801441.8428,
                              807451.8569]],
                            decimal=4)
        assert_almost_equal(y_coords[100:102, 220:223],
                            [[3954033.4223,
                              3954033.4223,
                              3954033.4223],
                             [3948023.4081,
                              3948023.4081,
                              3948023.4081]],
                            decimal=4)
        assert_almost_equal(pgrid.lsm.center,
                            [-106.6965833, 34.8059311])


def test_wrf_tiff_project(wrf, tgrid):
    """Test write wrf grid"""
    log_file = path.join(tgrid.output, 'wrf_tif.log')
    pa.log_to_file(filename=log_file, level='DEBUG')
    new_raster = path.join(tgrid.output, 'wrf_rainc_utm.tif')
    with wrf.xd as xd:
        pgrid = xd.lsm.to_utm('RAINC')
        pgrid.lsm.to_tif('RAINC', 3, new_raster)

    compare_rasters(path.join(tgrid.compare, 'wrf_rainc_utm.tif'), new_raster)
    pa.log_to_file(False)
    compare_log_file = path.join(tgrid.compare, 'wrf_tif.log')
    with open(log_file) as lgf, open(compare_log_file) as clgf:
        assert lgf.read() == clgf.read()
