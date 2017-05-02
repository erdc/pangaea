# -*- coding: utf-8 -*-
#
#  conftest.py
#  pangaea
#
#  Author : Alan D Snow, 2017.
#  License: BSD 3-Clause

import os

import pytest
from shutil import rmtree

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))


class TestDirectories(object):
    input =


@pytest.fixture(scope="module")
def tgrid(request):
    return os.path.join(SCRIPT_DIR, 'input')
