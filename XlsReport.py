#!/usr/bin/env python
# coding=utf-8

import os
import xlsxwriter


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def report(info):
    workbook = xlsxwriter.Workbook('report.xlsx')
    # ToDo: define the content of the xls.
