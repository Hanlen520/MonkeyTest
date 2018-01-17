#!/usr/bin/env python
# coding=utf-8

import os

class BaseAdb(object):
    """
    Fundamental operations of adb.
    """
    def adb_call(self, command):
        """
        get the command.
        """
        command_result = ''
        command_text = 'adb %s' % command
        print(command_text)
        results = os.popen(command_text, "r")
        while 1:
            line = results.readline()
            if not line: break
            command_result += line
        results.close()
        return command_result

    def attach_device(self):
        """
        check device, suport multi-devices
        """
        result = self.call_adb("devices")
        devices = result.partition('\n')[2].replace('\n', '').split('\tdevice')
        return [device for device in devices if len(device) > 2]

    def get_state(self):
        """
        check state.
        """
        result = self.call_adb("get-state")
        result = result.strip(' \t\n\r')
        return result or None
    
    def push(self, local, remote):
        """
        copy file from computer to phone.
        """
        result = self.call_adb("push %s %s" % (local, remote))
        return result
    
    def pull(self, remote, local):
        """
        frtch file from phone to computer.
        """
        result = self.call_adb("pull %s %s" % (remote, local))
        return result

    def open_app(self,packagename,activity,devices):
        """
        open pointed app.
        """
        result = self.call_adb("-s "+ devices+" shell am start -n %s/%s" % (packagename, activity))
        check = result.partition('\n')[2].replace('\n', '').split('\t ')
        if check[0].find("Error") >= 1:
            return False
        else:
            return True

    def get_app_pid(self, pkg_name):
        """
        get the pod by package name.
        """
        string = self.call_adb("shell ps | grep "+pkg_name)
        # print(string)
        if string == '':
            return "the process doesn't exist."
        result = string.split(" ")
        # print(result[4])
        return result[4]
