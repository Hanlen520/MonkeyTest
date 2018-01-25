#!/usr/bin/env python
# coding=utf-8

import os
import xlsxwriter
import BaseReport
import time

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file), p)
)

def report(info):
    workbook = xlsxwriter.Workbook('report.xlsx')
    bo = BaseReport.BaseReport(workbook)
    bo.monitor(info)
    bo.crash()
    bo.close()
