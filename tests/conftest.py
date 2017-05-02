# -*- coding: utf-8 -*-
#
#  conftest.py
#  pangaea
#
#  Author : Alan D Snow, 2017.
#  License: BSD 3-Clause

import os

import pytest

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope="module")
def tgrid(request):
    return os.path.join(SCRIPT_DIR, 'input')
