#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import argparse
import io
import ipaddress
import os
import sys
from datetime import datetime

import logbook
import pytablewriter as ptw
import six
import typepy
from typepy.type import (
    Bool, DateTime, Dictionary, Infinity, Integer, IpAddress, List, Nan, NoneType, NullString,
    RealNumber, String)


logbook.StderrHandler(
    level=logbook.DEBUG,
    format_string="[{record.level_name}] {record.channel}: {record.message}"
).push_application()

METHOD_HEADER = "Method"


class ExampleWriter(object):
    _METHOD_LIST = (
        "is_type",
        "validate",
        "convert",
        "try_convert",
        "force_convert",
    )


class ResultMatrixWriter(ExampleWriter):

    def __init__(self):
        self.typeclass = None
        self.strict_level = None
        self.header_list = None
        self.value_list = None

        self.__table_writer = ptw.RstSimpleTableWriter()
        self.__table_writer._dp_extractor.type_value_mapping = {
            NullString(None).typecode: '``""``',
            NoneType(None).typecode: "``None``",
            Infinity(None).typecode: '``Decimal("inf")``',
            Nan(None).typecode: '``Decimal("nan")``',
        }
        self.__table_writer._dp_extractor.const_value_mapping = {
            True: "``True``",
            False: "``False``",
            '``"127.0.0.1"``': '``ip_address("127.0.0.1")``',
        }

    def set_stream(self, output_stream):
        self.__table_writer.stream = output_stream

    def write_type_matrix(self):
        self.__table_writer.table_name = (
            ":py:class:`typepy.type.{0:s}`: :py:attr:`~typepy.type.{0:s}.strict_level` = {1:d}".format(
                self.typeclass.__name__, self.strict_level))
        self.__table_writer.header_list = self.header_list
        self.__table_writer.value_matrix = self.__get_result_matrix()
        if self.typeclass.__name__ in ["Dictionary", "List"]:
            self.__table_writer.type_hint_list = [
                String for _ in self.header_list
            ]

        self.__table_writer.write_table()
        self.__table_writer.write_null_line()

    def exeute(self, method, value):
        str_convert_type = (
            six.text_type, ipaddress.IPv4Address, ipaddress.IPv6Address)

        try:
            result = getattr(
                self.typeclass(value, self.strict_level), method)()

            if method == "validate":
                result = "NOP [#f1]_"
            elif isinstance(result, str_convert_type):
                result = '``"{}"``'.format(result)
        except TypeError:
            result = "E [#f2]_"
        except typepy.TypeConversionError:
            result = "E [#f3]_"

        return result

    def __get_result_matrix(self):
        result_matrix = []
        for method in self._METHOD_LIST:
            result_matrix.append(
                [
                    ":py:meth:`~.type.{:s}.{:s}`".format(
                        self.typeclass.__name__, method)
                ] + [
                    self.exeute(method, value)
                    for value in self.value_list
                ]
            )

        return result_matrix


class ResultMatrixManager(object):

    class ExampleBool(object):
        HEADER = [METHOD_HEADER] + [
            '``True``', '``"true"``', 1,
        ]
        VALUE = [
            True, "true", 1,
        ]

    class ExampleString(object):
        HEADER = [METHOD_HEADER] + [
            '``"abc"``', '``""``', '``"  "``', "``None``", 1,
        ]
        VALUE = [
            "abc", "", "  ", None, 1,
        ]

    class ExampleNumber(object):
        HEADER = [METHOD_HEADER] + [
            1, 1.0, 1.1,
            '``"1"``', '``"1.0"``', '``"1.1"``',
            "``True``",
        ]
        VALUE = [
            1, 1.0, 1.1, "1", "1.0", "1.1", True,
        ]

    class ExampleInfinity(object):
        HEADER = [METHOD_HEADER] + [
            '``float("inf")``', '``"Infinity"``', '``0.1``',
        ]
        VALUE = [
            float("inf"), "Infinity", 0.1,
        ]

    class ExampleNan(object):
        HEADER = [METHOD_HEADER] + [
            '``float("nan")``', '``"NaN"``', '``0.1``',
        ]
        VALUE = [
            float("nan"), "NaN", 0.1,
        ]

    class ExampleDateTime(object):
        HEADER = [METHOD_HEADER] + [
            '``datetime(2017, 1, 23, 4, 56)``',
            '``"2017-01-22T04:56:00+0900"``',
            "``1485685623``",
            '``"1485685623"``',
        ]
        VALUE = [
            datetime(2017, 1, 23, 4, 56),
            "2017-01-22T04:56:00+0900",
            1485685623,
            "1485685623",
        ]

    class ExampleIpAddress(object):
        HEADER = [METHOD_HEADER] + [
            "``ip_address('127.0.0.1')``",
            "``'127.0.0.1'``", "``'::1'``", "``'192.168.0.256'``", "``None``",
        ]
        VALUE = [
            ipaddress.ip_address("127.0.0.1"),
            "127.0.0.1", "::1", "192.168.0.256", None,
        ]

    class ExampleList(object):
        HEADER = [METHOD_HEADER] + [
            '``[]``',
            '``["a", "b"]``',
            '``{"a": 1}``',
            '``"abc"``',
        ]
        VALUE = [
            [],
            ["a", "b"],
            {"a": 1},
            "abc",
        ]

    class ExampleDictionary(object):
        HEADER = [METHOD_HEADER] + [
            '``{}``',
            '``{"a": 1}``',
            '``(("a", 1), )``',
        ]
        VALUE = [
            {},
            {"a": 1},
            (("a", 1), ),
        ]

    def __init__(self):
        self.strict_level_list = None

        self.__ewriter = ResultMatrixWriter()

    def set_stream(self, output_stream):
        self.__ewriter.set_stream(output_stream)

    def write_none(self):
        self.__ewriter.typeclass = NoneType
        self.__ewriter.header_list = self.ExampleString.HEADER
        self.__ewriter.value_list = self.ExampleString.VALUE
        self.__write()

    def write_ipaddress(self):
        self.__ewriter.typeclass = IpAddress
        self.__ewriter.header_list = self.ExampleIpAddress.HEADER
        self.__ewriter.value_list = self.ExampleIpAddress.VALUE
        self.__write()

    def write_bool(self):
        self.__ewriter.typeclass = Bool
        self.__ewriter.header_list = self.ExampleBool.HEADER
        self.__ewriter.value_list = self.ExampleBool.VALUE
        self.__write()

    def write_string(self):
        self.__ewriter.typeclass = String
        self.__ewriter.header_list = self.ExampleString.HEADER
        self.__ewriter.value_list = self.ExampleString.VALUE
        self.__write()

    def write_null_string(self):
        self.__ewriter.typeclass = NullString
        self.__ewriter.header_list = self.ExampleString.HEADER
        self.__ewriter.value_list = self.ExampleString.VALUE
        self.__write()

    def write_integer(self):
        self.__ewriter.typeclass = Integer
        self.__ewriter.header_list = self.ExampleNumber.HEADER
        self.__ewriter.value_list = self.ExampleNumber.VALUE
        self.__write()

    def write_realnumber(self):
        self.__ewriter.typeclass = RealNumber
        self.__ewriter.header_list = self.ExampleNumber.HEADER
        self.__ewriter.value_list = self.ExampleNumber.VALUE
        self.__write()

    def write_infinity(self):
        self.__ewriter.typeclass = Infinity
        self.__ewriter.header_list = self.ExampleInfinity.HEADER
        self.__ewriter.value_list = self.ExampleInfinity.VALUE
        self.__write()

    def write_nan(self):
        self.__ewriter.typeclass = Nan
        self.__ewriter.header_list = self.ExampleNan.HEADER
        self.__ewriter.value_list = self.ExampleNan.VALUE
        self.__write()

    def write_datetime(self):
        self.__ewriter.typeclass = DateTime
        self.__ewriter.header_list = self.ExampleDateTime.HEADER
        self.__ewriter.value_list = self.ExampleDateTime.VALUE
        self.__write()

    def write_list(self):
        self.__ewriter.typeclass = List
        self.__ewriter.header_list = self.ExampleList.HEADER
        self.__ewriter.value_list = self.ExampleList.VALUE
        self.__write()

    def write_dictionary(self):
        self.__ewriter.typeclass = Dictionary
        self.__ewriter.header_list = self.ExampleDictionary.HEADER
        self.__ewriter.value_list = self.ExampleDictionary.VALUE
        self.__write()

    def __write(self):
        for strict_level in self.strict_level_list:
            self.__ewriter.strict_level = strict_level
            self.__ewriter.write_type_matrix()


class PathMaker(object):

    def __init__(self, output_dir, encoding="utf8"):
        self.__output_dir = output_dir
        self.__encoding = encoding

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

    def open_write(self, filename):
        file_path = os.path.join(self.__output_dir, filename)
        print(file_path)

        return io.open(file_path, "w", encoding=self.__encoding)


def parse_option():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--type", choices=["reference", "example"])

    parser.add_argument(
        "-o", "--output-dir", default=".", required=True,
        help="default=%(default)s")

    return parser.parse_args()


def make_filename(name, prefix="matrix_", suffix="_type", extension=".txt"):
    return "{:s}{:s}{:s}{:s}".format(prefix, name, suffix, extension)


def write_result_matrix(output_dir_path):
    manager = ResultMatrixManager()
    opener = PathMaker(output_dir_path)

    manager.strict_level_list = (0,)
    with opener.open_write(make_filename("none")) as f:
        manager.set_stream(f)
        manager.write_none()

    manager.strict_level_list = (0, 1)
    with opener.open_write(make_filename("ipaddress")) as f:
        manager.set_stream(f)
        manager.write_ipaddress()

    with opener.open_write(make_filename("infinity")) as f:
        manager.set_stream(f)
        manager.write_infinity()

    with opener.open_write(make_filename("nan")) as f:
        manager.set_stream(f)
        manager.write_nan()

    with opener.open_write(make_filename("string")) as f:
        manager.set_stream(f)
        manager.write_string()

    with opener.open_write(make_filename("list")) as f:
        manager.set_stream(f)
        manager.write_list()

    with opener.open_write(make_filename("dictionary")) as f:
        manager.set_stream(f)
        manager.write_dictionary()

    with opener.open_write(make_filename("nullstring")) as f:
        manager.set_stream(f)
        manager.write_null_string()

    manager.strict_level_list = (0, 1, 2)
    with opener.open_write(make_filename("bool")) as f:
        manager.set_stream(f)
        manager.write_bool()

    with opener.open_write(make_filename("datetime")) as f:
        manager.set_stream(f)
        manager.write_datetime()

    with opener.open_write(make_filename("integer")) as f:
        manager.set_stream(f)
        manager.write_integer()

    with opener.open_write(make_filename("realnumber")) as f:
        manager.set_stream(f)
        manager.write_realnumber()


def write_example(output_dir_path):
    opener = PathMaker(output_dir_path)


def main():
    options = parse_option()

    # ptw.set_log_level(logbook.DEBUG)

    write_result_matrix(options.output_dir)
    write_example(options.output_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
