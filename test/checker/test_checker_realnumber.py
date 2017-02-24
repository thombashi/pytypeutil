# encoding: utf-8


"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import unicode_literals

from decimal import Decimal
import itertools

import pytest
import six

from pytypeutil import (
    Typecode,
    StrictLevel,
)
from pytypeutil.type import RealNumber


nan = float("nan")
inf = float("inf")


class Test_RealNumber_is_type:

    @pytest.mark.parametrize(
        ["value", "strict_level", "expected"],
        list(itertools.product(
            [
                0, 0.0, 0., six.MAXSIZE, -six.MAXSIZE,
                str(six.MAXSIZE), str(-six.MAXSIZE), "0.1", "-0.1", "1e-05",
            ],
            [StrictLevel.MIN],
            [True],
        )) + list(itertools.product(
            [True, inf, nan, "", "0xf"],
            [StrictLevel.MIN],
            [False],
        )) + list(itertools.product(
            [
                0, 0.0, 0., six.MAXSIZE, -six.MAXSIZE,
            ],
            [StrictLevel.MIN + 1],
            [False],
        )) + list(itertools.product(
            [
                0, 0.0, 0., six.MAXSIZE, -six.MAXSIZE, "1.0",
                str(six.MAXSIZE), str(-six.MAXSIZE), "0.1", "-0.1", "1e-05",
            ],
            [StrictLevel.MAX],
            [False],
        )) + list(itertools.product(
            [0.1, -0.1, .5, Decimal("1.1")],
            [StrictLevel.MIN, StrictLevel.MIN + 1,  StrictLevel.MAX],
            [True],
        ))
    )
    def test_normal(self, value, strict_level, expected):
        type_checker = RealNumber(value, strict_level)

        assert type_checker.is_type() == expected
        assert type_checker.typecode == Typecode.FLOAT