# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import pytest

import typepy

from ._common import convert_wrapper


nan = float("nan")
inf = float("inf")


class Test_Integer(object):
    @pytest.mark.parametrize(
        ["method", "strict_level", "value", "expected"],
        [
            ["convert", 0, 1, 1],
            ["convert", 0, 1.0, 1],
            ["convert", 0, 1.1, 1],
            ["convert", 0, "0", 0],
            ["convert", 0, "1.0", 1],
            ["convert", 0, "1.1", 1],
            ["convert", 0, 9223372036854775807, 9223372036854775807],
            ["convert", 0, True, 1],
            ["convert", 0, None, "E"],
            ["convert", 0, inf, "E"],
            ["convert", 0, nan, "E"],
            ["convert", 0, "test", "E"],
            ["convert", 0, "", "E"],
            ["convert", 1, 1, 1],
            ["convert", 1, 1.0, 1],
            ["convert", 1, 1.1, "E"],
            ["convert", 1, "0", 0],
            ["convert", 1, "1.0", 1],
            ["convert", 1, "1.1", "E"],
            ["convert", 1, 9223372036854775807, 9223372036854775807],
            ["convert", 1, True, "E"],
            ["convert", 1, None, "E"],
            ["convert", 1, inf, "E"],
            ["convert", 1, nan, "E"],
            ["convert", 1, "test", "E"],
            ["convert", 1, "", "E"],
            ["convert", 2, 1, 1],
            ["convert", 2, 1.0, "E"],
            ["convert", 2, 1.1, "E"],
            ["convert", 2, "0", "E"],
            ["convert", 2, "1.0", "E"],
            ["convert", 2, "1.1", "E"],
            ["convert", 2, 9223372036854775807, 9223372036854775807],
            ["convert", 2, True, "E"],
            ["convert", 2, None, "E"],
            ["convert", 2, inf, "E"],
            ["convert", 2, nan, "E"],
            ["convert", 2, "test", "E"],
            ["convert", 2, "", "E"],
            ["try_convert", 0, 1, 1],
            ["try_convert", 0, 1.0, 1],
            ["try_convert", 0, 1.1, 1],
            ["try_convert", 0, "0", 0],
            ["try_convert", 0, "1.0", 1],
            ["try_convert", 0, "1.1", 1],
            ["try_convert", 0, 9223372036854775807, 9223372036854775807],
            ["try_convert", 0, True, 1],
            ["try_convert", 0, None, None],
            ["try_convert", 0, inf, None],
            ["try_convert", 0, nan, None],
            ["try_convert", 0, "test", None],
            ["try_convert", 0, "", None],
            ["try_convert", 1, 1, 1],
            ["try_convert", 1, 1.0, 1],
            ["try_convert", 1, 1.1, None],
            ["try_convert", 1, "0", 0],
            ["try_convert", 1, "1.0", 1],
            ["try_convert", 1, "1.1", None],
            ["try_convert", 1, 9223372036854775807, 9223372036854775807],
            ["try_convert", 1, True, None],
            ["try_convert", 1, None, None],
            ["try_convert", 1, inf, None],
            ["try_convert", 1, nan, None],
            ["try_convert", 1, "test", None],
            ["try_convert", 1, "", None],
            ["try_convert", 2, 1, 1],
            ["try_convert", 2, 1.0, None],
            ["try_convert", 2, 1.1, None],
            ["try_convert", 2, "0", None],
            ["try_convert", 2, "1.0", None],
            ["try_convert", 2, "1.1", None],
            ["try_convert", 2, 9223372036854775807, 9223372036854775807],
            ["try_convert", 2, True, None],
            ["try_convert", 2, None, None],
            ["try_convert", 2, inf, None],
            ["try_convert", 2, nan, None],
            ["try_convert", 2, "test", None],
            ["try_convert", 2, "", None],
            ["force_convert", 0, 1, 1],
            ["force_convert", 0, 1.0, 1],
            ["force_convert", 0, 1.1, 1],
            ["force_convert", 0, "0", 0],
            ["force_convert", 0, "1.0", 1],
            ["force_convert", 0, "1.1", 1],
            ["force_convert", 0, 9223372036854775807, 9223372036854775807],
            ["force_convert", 0, True, 1],
            ["force_convert", 0, None, "E"],
            ["force_convert", 0, inf, "E"],
            ["force_convert", 0, nan, "E"],
            ["force_convert", 0, "test", "E"],
            ["force_convert", 0, "", "E"],
            ["force_convert", 1, 1, 1],
            ["force_convert", 1, 1.0, 1],
            ["force_convert", 1, 1.1, 1],
            ["force_convert", 1, "0", 0],
            ["force_convert", 1, "1.0", 1],
            ["force_convert", 1, "1.1", 1],
            ["force_convert", 1, 9223372036854775807, 9223372036854775807],
            ["force_convert", 1, True, 1],
            ["force_convert", 1, None, "E"],
            ["force_convert", 1, inf, "E"],
            ["force_convert", 1, nan, "E"],
            ["force_convert", 1, "test", "E"],
            ["force_convert", 1, "", "E"],
            ["force_convert", 2, 1, 1],
            ["force_convert", 2, 1.0, 1],
            ["force_convert", 2, 1.1, 1],
            ["force_convert", 2, "0", 0],
            ["force_convert", 2, "1.0", 1],
            ["force_convert", 2, "1.1", 1],
            ["force_convert", 2, 9223372036854775807, 9223372036854775807],
            ["force_convert", 2, True, 1],
            ["force_convert", 2, None, "E"],
            ["force_convert", 2, inf, "E"],
            ["force_convert", 2, nan, "E"],
            ["force_convert", 2, "test", "E"],
            ["force_convert", 2, "", "E"],
        ],
    )
    def test_normal(self, method, strict_level, value, expected):
        assert convert_wrapper(typepy.Integer(value, strict_level), method) == expected
