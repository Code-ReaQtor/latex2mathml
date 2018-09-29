#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2018, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __license__ = "MIT"
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
# __status__ = "Production"
import xml.etree.cElementTree as eTree

# noinspection PyPackageRequirements
import pytest

# noinspection PyProtectedMember
from latex2mathml.converter import convert, _convert


@pytest.fixture
def math_and_row():
    math = eTree.Element('math')
    row = eTree.SubElement(math, 'mrow')
    yield math, row


def test_single_identifier(math_and_row):
    math, row = math_and_row
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'x'
    assert _convert(math) == convert('x')


def test_multiple_identifiers(math_and_row):
    math, row = math_and_row
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'x'
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'y'
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'z'
    assert _convert(math) == convert('xyz')


def test_single_number(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '3'
    assert _convert(math) == convert('3')


def test_multiple_numbers(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '333'
    assert _convert(math) == convert('333')


def test_decimal_numbers(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '12.34'
    assert _convert(math) == convert('12.34')


def test_numbers_and_identifiers(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '12'
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'x'
    assert _convert(math) == convert('12x')


def test_single_operator(math_and_row):
    math, row = math_and_row
    mo = eTree.SubElement(row, 'mo')
    mo.text = '&#x0002B;'
    assert _convert(math) == convert('+')


def test_numbers_and_operators(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '3'
    mo = eTree.SubElement(row, 'mo')
    mo.text = '&#x02212;'
    mn = eTree.SubElement(row, 'mn')
    mn.text = '2'
    assert _convert(math) == convert('3-2')


def test_numbers_and_identifiers_and_operators(math_and_row):
    math, row = math_and_row
    mn = eTree.SubElement(row, 'mn')
    mn.text = '3'
    mi = eTree.SubElement(row, 'mi')
    mi.text = 'x'
    mo = eTree.SubElement(row, 'mo')
    mo.text = '&#x0002A;'
    mn = eTree.SubElement(row, 'mn')
    mn.text = '2'
    assert _convert(math) == convert('3x*2')


def test_single_group(math_and_row):
    math, row = math_and_row
    mrow = eTree.SubElement(row, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'a'
    assert _convert(math) == convert('{a}')


def test_multiple_groups(math_and_row):
    math, row = math_and_row
    mrow = eTree.SubElement(row, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'a'
    mrow = eTree.SubElement(row, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'b'
    assert _convert(math) == convert('{a}{b}')


def test_inner_group(math_and_row):
    math, row = math_and_row
    mrow = eTree.SubElement(row, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'a'
    mo = eTree.SubElement(mrow, 'mo')
    mo.text = '&#x0002B;'
    mrow = eTree.SubElement(mrow, 'mrow')
    mi = eTree.SubElement(mrow, 'mi')
    mi.text = 'b'
    assert _convert(math) == convert('{a+{b}}')


def test_over(math_and_row):
    math, row = math_and_row
    frac = eTree.SubElement(row, 'mfrac')
    row = eTree.SubElement(frac, 'mrow')
    mn = eTree.SubElement(row, 'mn')
    mn.text = '1'
    row = eTree.SubElement(frac, 'mrow')
    mn = eTree.SubElement(row, 'mn')
    mn.text = '2'
    assert _convert(math) == convert(r'1 \over 2')
    assert convert(r'1 \over 2') == convert(r'{1 \over 2}')

