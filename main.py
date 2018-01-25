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
import BaseReport
from  BaseWriteReport import report

from BasePickle import readInfo
from BasePickle import writeInfo
from BasePickle import writeSum
from File import base_file

#PATH = lambda p: os.path.abspath(
    #os.path.join(os.path.dirname(__file__), p)
#)

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(os.path.realpath('__file__')), p)) #os.path.realpath(path)  返回path的真实路径

ba = BaseAdb.BaseAdb()
info = []


def create_file(dev, app, data):
    """
    Create the info file
    """
    print("创建持久性文件...")
    base_file(PATH("./info/sumInfo.pickle")).mkdir_file() # 用于记录是否已经测试完毕，里面存的是一个整数
    base_file(PATH("./info/info.pickle")).mkdir_file() # 用于记录统计结果的信息，是[{}]的形式
    writeSum(0, data, PATH("./info/sumInfo.pickle")) # 初始化记录当前真实连接的设备数
    app[dev] = {"header": {"phone_name": dev}}

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
    create_file(devices, app, num)
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
                writeSum(1, path=PATH("./info/sumInfo.pickle"))
                app[devices]["header"]["monkey_log"] = mc["monkey_log"]
                writeInfo(app, PATH("./info/info.pickle"))
                break

    if readInfo(PATH("./info/sumInfo.pickle")) <= 0:
        report(readInfo(PATH("./info/info.pickle")))
        print("Kill adb server,test finished！")

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
