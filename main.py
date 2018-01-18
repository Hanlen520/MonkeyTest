#!/usr/bin/env python
# coding=utf-8

import pickle
import subprocess
import shutil
import threading
import os
import datetime
import uuid
import time

from multiprocessing import Process
from multiprocessing import Pool

import BaseAdb
import MonkeyConfig

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

ba = BaseAdb.BaseAdb()
info = []

def runtest():
    """
    start the test.
    """
    shutil.rmtree((PATH("./info/")))
    os.makedirs((PATH("./info/")))
    devices_pool = []
    devices = ba.attach_device()
    if devices:
        for item in range(0, len(devices)):
            _app = {}
            _app["devices"] = devices[item]
            _app["num"] = len(devices)
            devices_pool.append(_app)
        pool = Pool(len(devices))
        pool.map(start, devices_pool)
        pool.close()
        pool.join()
    else:
        print("No devices")

def start(devicess):
    devices = devicess["devices"]
    num = devicess["num"]
    app = {}
    mc = MonkeyConfig.monkeyConfig((PATH("monkey.ini")))
    mc["log"] = PATH("./log") + "/"
    mc["monkey_log"] = mc["log"] + "monkey.log"
    mc["cmd"] = mc["cmd"] + mc["monkey_log"]
    start_monkey("adb -s " + devices + " shell " + mc["cmd"], mc["log"])
    time.sleep(1)
    
    while True:
        with open(mc["monkey_log"], encoding = "utf-8") as monkeylog:
            time.sleep(1)
            if monkeylog.read().count('Monkey finished') > 0 :
                print(str(devices) + "  Test End.")
                break

def start_monkey(cmd, log):
    """
    start module.
    """
    os.popen(cmd)
    print(cmd)

    logcatname = log + r"traces.log"
    cmd2 = "adb logcat -d >%s" % (logcatname)
    os.popen(cmd2)

    # export the traces file
    tracesname = log + r"traces.log"
    cmd3 = "adb shell cat /data/anr/traces.txt>%s" % tracesname
    os.popen(cmd3)


runtest()
