# -*- coding: utf-8 -*-
#
#  conftest.py
#  pangaea
#
#  Author : Alan D Snow, 2017.
#  License: BSD 3-Clause

import os

from numpy import array
from numpy.testing import assert_almost_equal
from osgeo import gdal
import pytest

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

def compare_proj4(original, new):
    """compare proj4 strings"""

    def to_dict(proj4_str):
        """convert to dictionary"""
        proj4_split = proj4_str.strip().split(" ")
        proj4_dict = dict()
        for elem in proj4_split:
            elem_split = elem.strip().split("=")
            try:
                key, value = elem_split
            except ValueError:
                key = elem
                value = None
            proj4_dict[key] = value
        return proj4_dict

    orig_dict = to_dict(original)
    new_dict = to_dict(new)

    assert orig_dict.keys() == new_dict.keys()
    for key, value in orig_dict.items():
        try:
            assert_almost_equal(float(orig_dict[key]),
                                float(new_dict[key]))
        except (ValueError, TypeError):
            assert orig_dict[key] == new_dict[key]

def compare_rasters(original, new, precision=7):
    """compare two rasters"""
    ds_o = gdal.Open(original)
    ds_n = gdal.Open(new)

    # compare data
    r_o = array(ds_o.ReadAsArray())
    r_n = array(ds_n.ReadAsArray())
    assert_almost_equal(r_o, r_n, decimal=precision)

    # compare geotransform
    assert_almost_equal(ds_o.GetGeoTransform(),
                        ds_n.GetGeoTransform(),
                        decimal=9)

    # compare band counts
    assert ds_o.RasterCount == ds_n.RasterCount
    # compare nodata
    for band_id in range(1, ds_o.RasterCount + 1):
        assert (ds_o.GetRasterBand(band_id).GetNoDataValue() ==
                ds_n.GetRasterBand(band_id).GetNoDataValue())

class TestDirectories(object):
    input = os.path.join(SCRIPT_DIR, 'input')
    compare = os.path.join(SCRIPT_DIR, 'compare')
    output = os.path.join(SCRIPT_DIR, 'output')

    def clean(self):
        """
        Clean out test directory
        """
        os.chdir(self.output)

        # Clear out directory
        file_list = os.listdir(self.output)

        for afile in file_list:
            if not afile.endswith('.gitignore'):
                path = os.path.join(self.output, afile)
                if os.path.isdir(path):
                    rmtree(path)
                else:
                    os.remove(path)

@pytest.fixture(scope="module")
def tread(request):
    return TestDirectories.input

@pytest.fixture(scope="module")
def tgrid(request):
    _td = TestDirectories()
    _td.clean()

    yield _td

    _td.clean()
